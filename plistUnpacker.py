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
        if item.tag =='key':
            if tree[index+1].tag == 'string':
                d[item.text] = tree[index+1].text
            elif tree[index+1].tag == 'true':
                d[item.text]=True
            elif tree[index+1].tag == 'false':
                d[item.text]=False
            elif  tree[index+1].tag == "integer":
                d[item.text]=tree[index+1].text
            elif  tree[index+1].tag == "array":
                d[item.text]=tree[index+1].text
            elif tree[index+1].tag == 'dict':
                d[item.text] = tree_to_dict(tree[index+1])
    return d
def gen_png(plist_filename,png_filename):
    format = None
    root = ElementTree.fromstring(open(plist_filename,'r').read())
    plist_dict = tree_to_dict(root[0])
    if plist_dict.has_key("metadata") and plist_dict["metadata"].has_key("format"):
        format = int(plist_dict["metadata"]["format"])
    if format == 0:
        gen_plist_format_2(plist_dict,png_filename)
    elif format == 1 or format == 2:
        gen_plist_format_1(plist_dict,png_filename)
    elif format == 3:
        gen_plist_format_3(plist_dict,png_filename)
    print format
    print "gen_png"

def gen_plist_format_1(plist_dict,png_filename):
    baseName = os.path.basename(png_filename)
    baseName = baseName[0:baseName.index('.')]
    file_path = os.path.join(os.path.dirname(png_filename),baseName)

    big_image = Image.open(png_filename)
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

def gen_plist_format_2(plist_dict,png_filename):
    baseName = os.path.basename(png_filename)
    baseName = baseName[0:baseName.index('.')]
    file_path = os.path.join(os.path.dirname(png_filename),baseName)
    big_image = Image.open(png_filename)

    to_list = lambda x:x.replace('{','').replace('}','').split(',')
    for k,v in plist_dict['frames'].items():

        x = int(v['x'])
        y = int(v['y'])
        width = int(v['width'])
        height = int(v['height'])
        box = (
            int(x),
            int(y),
            int(x + width),
            int(y + height)
        )
        rect_on_big = big_image.crop(box)
        # rect_on_big.show()
        result_box=(
                width,
                height
            )
        result_image = Image.new('RGBA',result_box,(0,0,0,0))
        outfile = (file_path+'/'+k)
        outpath = os.path.dirname(outfile)
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        #outfile=outfile+'.png'
        print outfile,"generated"
        rect_on_big.save(outfile)

def gen_plist_format_3(plist_dict,png_filename):
    baseName = os.path.basename(png_filename)
    baseName = baseName[0:baseName.index('.')]
    file_path = os.path.join(os.path.dirname(png_filename),baseName)
    big_image = Image.open(png_filename)

    to_list = lambda x:x.replace('{','').replace('}','').split(',')

    for k,v in plist_dict['frames'].items():
        rectlist = to_list(v['textureRect'])
        width = int(rectlist[3] if v['textureRotated'] else rectlist[2])
        height = int(rectlist[2] if v['textureRotated'] else rectlist[3])
        box = (
            int(rectlist[0]),
            int(rectlist[1]),
            int(rectlist[0]) + width,
            int(rectlist[1]) + height,
        )
        sizelist = [int(x)for x in to_list(v['spriteSize'])]
        rect_on_big = big_image.crop(box)
        if v['textureRotated']:
            rect_on_big = rect_on_big.transpose(Image.ROTATE_90)
        result_image = Image.new('RGBA',sizelist,(0,0,0,0))
        offset = [float(x)for x in to_list(v['spriteOffset'])]
        orsize = [int(x)for x in to_list(v['spriteSourceSize'])]
        width = orsize[0]
        height = orsize[1]
        print orsize
        result_box=(
            int(offset[0]),
            int(offset[1])
        )

        result_image.paste(rect_on_big,result_box)
        outfile = (file_path+'/'+k)
        outpath = os.path.dirname(outfile)
        if not os.path.exists(outpath):
            os.makedirs(outpath)
        #outfile=outfile+'.png'
        print outfile,"generated"
        result_image.save(outfile)
    print "gen_plist_format_3"

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
                    gen_png(plist_filename,png_filename)
                else:
                    print"make sure you have both %s plist and png files in the same directory" %plist_filename
        else:
            if endWith(pathOrFilename,'.plist'):
                newFileName = pathOrFilename[0:pathOrFilename.find('.plist')]
                plist_filename =newFileName +'.plist'
                png_filename = newFileName +'.png'
                gen_png(plist_filename,png_filename)
            else:
                print "USAGE: python plistUnpacker.py [Directory/***.plist]"
