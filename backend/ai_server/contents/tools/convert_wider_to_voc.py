import shutil
from skimage import io

headstr = """\
<annotation>
    <folder>VOC2012</folder>
    <filename>%06d.jpg</filename>
    <source>
        <database>My Database</database>
        <annotation>PASCAL VOC2012</annotation>
        <image>flickr</image>
        <flickrid>NULL</flickrid>
    </source>
    <owner>
        <flickrid>NULL</flickrid>
        <name>company</name>
    </owner>
    <size>
        <width>%d</width>
        <height>%d</height>
        <depth>%d</depth>
    </size>
    <segmented>0</segmented>
"""

objstr = """\
    <object>
        <name>%s</name>
        <pose>Unspecified</pose>
        <truncated>0</truncated>
        <difficult>0</difficult>
        <bndbox>
            <xmin>%d</xmin>
            <ymin>%d</ymin>
            <xmax>%d</xmax>
            <ymax>%d</ymax>
        </bndbox>
    </object>
"""

tailstr = '''\
</annotation>
'''


def writexml(idx, im, bbxes):
    height, width = im.shape[0], im.shape[1]
    filename = ("../datasets/WIDER_Face/VOCdevkit/VOC2012/Annotations/%06d.xml" % (idx))

    # head
    f = open(filename, "w")
    head = headstr % (idx, im.shape[1], im.shape[0], im.shape[2])
    f.write(head)

    # object
    for bbx in bbxes:
        xmin = min(bbx[0], width - 1)
        ymin = min(bbx[1], height - 1)
        xmax = min(bbx[0] + bbx[2], width - 1)
        ymax = min(bbx[1] + bbx[3], height - 1)

        if xmin == xmax or ymin == ymax:
            continue

        f.write(objstr % ('face', xmin, ymin, xmax, ymax))

    # tail
    f.write(tailstr)

    f.close()


def clear_dir():
    if shutil.os.path.exists(('../datasets/WIDER_Face/VOCdevkit')):
        shutil.rmtree(('../datasets/WIDER_Face/VOCdevkit'))

    shutil.os.mkdir(('../datasets/WIDER_Face/VOCdevkit'))
    shutil.os.mkdir(('../datasets/WIDER_Face/VOCdevkit/VOC2012'))
    shutil.os.mkdir(('../datasets/WIDER_Face/VOCdevkit/VOC2012/Annotations'))
    shutil.os.makedirs(('../datasets/WIDER_Face/VOCdevkit/VOC2012/ImageSets/Main'))
    shutil.os.mkdir(('../datasets/WIDER_Face/VOCdevkit/VOC2012/JPEGImages'))


def excute_datasets(idx, datatype):
    # ????????? ?????? ?????? ???????????? ?????? ?????? ????????????
    f = open(('../datasets/WIDER_Face/VOCdevkit/VOC2012/ImageSets/Main/' + datatype + '.txt'), 'a')

    # ??? ???????????? ?????? ?????? ???????????? ?????? ?????? ?????? ????????????
    f_bbx = open(('../datasets/WIDER_Face/wider_face_split/wider_face_' + datatype + '_bbx_gt.txt'), 'r')

    valid_image = 0
    invalid_image = 0
    max_nums = 0

    while True:
        filename = f_bbx.readline().strip('\n')

        if not filename:
            break

        # ????????? ????????????
        im = io.imread(('../datasets/WIDER_Face/WIDER_' + datatype + '/images/' + filename))

        # ?????? ??????
        nums = int(f_bbx.readline().strip())

        # ?????? ?????? ????????? ??????
        if nums > max_nums:
            max_nums = nums

        bbxes = []

        # ???????????? ????????? ?????? ?????? ????????????
        if nums == 0:
            invalid_image += 1
            bbx_info = f_bbx.readline()
            continue

        valid_image += 1

        # ?????? ??????
        # x1, y1, w, h, blur, expression, illumination, invalid, occlusion, pose
        for ind in range(nums):
            # ?????? ?????? ?????? ????????????
            bbx_info = f_bbx.readline().strip(' \n').split(' ')

            # ??????????????? ??????
            bbx = [int(bbx_info[i]) for i in range(len(bbx_info))]

            # ????????? ?????? ????????? ??????
            if bbx[7] == 0:
                bbxes.append(bbx)

        # xml ??????
        writexml(idx, im, bbxes)

        # ????????? ????????????
        shutil.copyfile(('../datasets/WIDER_Face/WIDER_' + datatype + '/images/' + filename), ('../datasets/WIDER_Face/VOCdevkit/VOC2012/JPEGImages/%06d.jpg' % (idx)))

        # ????????? ?????? ?????? ??????
        f.write('%06d\n' % (idx))
        idx += 1

    f.close()
    f_bbx.close()

    print("data:{} invalid_image:{} valid_image:{} max_nums:{}".format(datatype, invalid_image, valid_image, max_nums))

    return idx


if __name__ == '__main__':
    clear_dir()
    idx = 1
    idx = excute_datasets(idx, 'train')
    idx = excute_datasets(idx, 'val')
    print('Complete...')
