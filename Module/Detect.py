from paddleocr import PaddleOCR, draw_ocr


from DButil import MyDButil


class MyDetect:
    def __init__(self, table_name):
        self.db = MyDButil()
        self.table_name = table_name

    # 生成对比结果
    def Detect_Result(self, boxes, texts):
        digit = []
        coords = []
        for txt in texts:
            if txt.isdigit():
                digit.append(txt)
                index = texts.index(txt)  # 当前文本是数字的索引，对应到坐标去
                coords.append(boxes[index])
        print("筛选后的数字", digit, "筛选后的位置", coords)
        rect1 = []
        rect2 = []

        sql = "select * from " + self.table_name + ";"
        self.result = self.db.fetch_all(sql)
        for info in self.result:
            temp = []
            temp.append(int(info[1]))
            temp.append(int(info[2]))
            temp.append(int(info[3]) + int(info[1]))
            temp.append(int(info[4]) + int(info[2]))
            rect1.append(temp)
        for info in coords:
            temp = []
            temp.append(info[0][0])
            temp.append(info[0][1])
            temp.append(info[2][0])
            temp.append(info[2][1])
            rect2.append(temp)

        max_intersect = []
        for sample_rect in rect1:
            # 列表存放intersect值和当前检测结果的索引
            intersect_list = []
            for rect in rect2:
                intersect = self.compute_iou(sample_rect, rect)
                intersect_list.append([intersect, rect2.index(rect)])
            max_intersect.append(max(intersect_list))
        return max_intersect




    # 计算最大重叠面积
    def compute_iou(self, rect1, rect2):
        S_rect1 = (rect1[2] - rect1[0]) * (rect1[3] - rect1[1])
        S_rect2 = (rect2[2] - rect2[0]) * (rect2[3] - rect2[1])

        #   寻找边缘
        left_line = max(rect1[0], rect2[0])  # 最大的x0
        right_line = min(rect1[2], rect2[2])  # 最小的x1
        top_line = max(rect1[1], rect2[1])  # 最大的y0
        bottom_line = min(rect1[3], rect2[3])  # 最小的y1

        # 判断两个矩形是否相交
        if left_line >= right_line or top_line >= bottom_line:
            return 0
        else:
            intersect = (right_line - left_line) * (bottom_line - top_line)
            return intersect

    def detect_OCR(self, img):
        # Paddleocr目前支持中英文、英文、法语、德语、韩语、日语，可以通过修改lang参数进行切换
        # 参数依次为`ch`, `en`, `french`, `german`, `korean`, `japan`。
        ocr = PaddleOCR(use_angle_cls=True, use_gpu=False, lang="ch", use_space_char=True,
                        det_db_unclip_ratio=2.5)  # det_db_unclip_ratio=2.5这是参数定义位置，这个参数是检测后处理时控制文本框大小的，默认2.0，可以尝试改成2.5或者更大，反之，如果觉得文本框不够紧凑，也可以把该参数调小。 need to run only once to download and load model into memory
        img_path = '1.jpg'
        result = ocr.ocr(img_path, cls=True)
        for line in result:
            print(line)

        # 显示结果
        from PIL import Image
        image = Image.open(img_path).convert('RGB')
        boxes = [line[0] for line in result]
        txts = [line[1][0] for line in result]
        scores = [line[1][1] for line in result]
        im_show = draw_ocr(image, boxes, txts, scores, font_path='/path/to/PaddleOCR/doc/simfang.ttf')
        im_show = Image.fromarray(im_show)
        im_show.save('result.jpg')
        return boxes, scores
