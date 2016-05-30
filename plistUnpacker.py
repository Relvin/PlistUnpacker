#!python
import os,sys
from xml.etree import ElementTree
from PIL import Image
def endWith(s,*endstring):
    array = map(s.endswith,endstring)
    if True in array:
        return True
    else:
        return False

def get_recursive_file_list(path):
    current_files = os.listdir(path)
    all_files=[]
    for file_name in current_files:
        full_file_name=os.path.join(path,file_name)
        if endWith(full_file_name,'.plist'):
            full_file_name=full_file_name.replace('.plist','')
            all_files.append(full_file_name)
        if os.path.isdir(full_file_name):
            next_level_files = get_recursive_file_list(full_file_name)
            all_files.extend(next_level_files)
    return all_files

def tree_to_dict(tree):
    d={}
    for index,item in enumerate(tree):
        if item.tag=='key':
            if tree[index+1].tag == 'string':
                d[item.text] = tree[index+1].text
            elif tree[index+1].tag == 'true':
                d[item.text]=True
            elif tree[index+1].tag == 'false':
                d[item.text]=False
            elif tree[index+1].tag == 'dict':
                d[item.text]=tree_to_dict(tree[index+1])
    return d

def gen_png_from_plist(plist_filename,png_filename):
    file_path = plist_filename.replace('.plist','')
    big_image = Image.open(png_filename)
    root = ElementTree.fromstring(open(plist_filename,'r').read())
    plist_dict = tree_to_dict(root[0])
    to_list = lambda x:x.replace('{','').replace('}','').split(',')
    for k,v in plist_dict['frames'].items():
        rectlist = to_list(v['frame'])
        width = int(rectlist[3] if v['rotated'] else rectlist[2])
        height = int(rectlist[2] if v['rotated'] else rectlist[3])
        box = (
            int(rectlist[0]),
            int(rectlist[1]),
            int(rectlist[0])+width,
            int(rectlist[1])+height,
        )
        sizelist = [int(x)for x in to_list(v['sourceSize'])]
        rect_on_big = big_image.crop(box)
        if v['rotated']:
            rect_on_big = rect_on_big.transpose(Image.ROTATE_90)
        result_image = Image.new('RGBA',sizelist,(0,0,0,0))
        offset = [int(x)for x in to_list(v['offset'])]
        if v['rotated']:
            result_box=(
                (sizelist[0] - height) / 2 + offset[0],
                (sizelist[1] - width) / 2 + offset[1],
            )
        else:
            result_box=(
                (sizelist[0] - width)/2 + offset[0],
                (sizelist[1] - height)/2 + offset[1]
            )
        result_image.paste(rect_on_big,result_box)
        outfile = (file_path+'/'+k)
        outpath = os.path.dirname(outfile)
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        #outfile=outfile+'.png'
        print outfile,"generated"
        result_image.save(outfile)

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print "USAGE: python plistUnpacker.py [Directory/xxx.plist]"
    else:
        pathOrFilename = sys.argv[1]
        if os.path.isdir(pathOrFilename):
            allPlistArray = get_recursive_file_list(pathOrFilename)
            for plist in allPlistArray:
                filename = plist
                plist_filename =filename+'.plist'
                png_filename = filename+'.png'
                if(os.path.exists(plist_filename) and os.path.exists(png_filename)):
                    gen_png_from_plist(plist_filename,png_filename)
                else:
                    print"make sure you have both plist and png files in the same directory"
        else:
            if endWith(pathOrFilename,'.plist'):
                newFileName = pathOrFilename[0:pathOrFilename.find('.plist')]
                plist_filename =newFileName +'.plist'
                png_filename = newFileName +'.png'
                gen_png_from_plist(plist_filename,png_filename)
            else:
                print "USAGE: python plistUnpacker.py [Directory/***.plist]"
