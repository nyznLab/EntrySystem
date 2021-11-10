import xml.sax


class ScaleHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        super().__init__()
        self.scaleContent = {}
        self.currentQuestionIndex = -1
        self.CurrentData = ""

    # 元素开始事件处理
    # {
    #     "title": "量表名",
    #     "warn": "量表警告语",
    #     "1": {
    #         "title": "题目文本内容",
    #         "options": [
    #             {
    #                 "type": "radio",
    #                 "name": "question1",
    #                 "value": "1",
    #                 "content": "选项一的文本内容",
    #             },
    #             {
    #                 "type": "radio",
    #                 "name": "question1",
    #                 "value": "2",
    #                 "content": "选项二的文本内容",
    #             },
    #             {
    #                 "type": "radio",
    #                 "name": "question1",
    #                 "value": "3",
    #                 "content": "选项三的文本内容",
    #             },
    #             {
    #                 "type": "radio",
    #                 "name": "question1",
    #                 "value": "4",
    #                 "content": "选项四的文本内容",
    #             },
    #         ],
    #         "rule": "题目的规则",
    #     },
    #     "2": {
    #
    #     },
    # }
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "scale":
            # 处理scale标签
            self.scaleContent["title"] = attributes["title"]
            self.scaleContent["warn"] = attributes["warn"]
        if tag == "question":
            # 处理 question标签 是一个字典
            # key是当前题目的index value中option字段是option标签组成的数组（这里先为option字段创建一个空数组），title为题目的内容
            # xml是按照顺序加载的 这里先暂存一下当前题号 方便后面处理option标签
            self.currentQuestionIndex = attributes["index"]
            self.scaleContent[attributes["index"]] = {
                "title": attributes["title"],
                "options": [],
            }
            # 如果有rule标签的话 在题目字典中加入一个rule字段
            if "rule" in attributes.keys():
                self.scaleContent[attributes["index"]]["rule"] = attributes["rule"]
        if tag == "option":
            # 处理option标签 在上面创建的option数组中加入option字典，两个字段 type 和 name
            self.scaleContent[self.currentQuestionIndex]["options"].append(
                {
                    "type": attributes["type"],
                    "name": attributes["name"],
                }
            )
            # 处理value标签
            if "value" in attributes.keys():
                self.scaleContent[self.currentQuestionIndex]["options"][-1]["value"] = attributes["value"]

    # 内容事件处理
    def characters(self, content):
        # 加载选项的文本内容
        if self.CurrentData == "option" and str(content).strip() != "":
            self.scaleContent[self.currentQuestionIndex]["options"][-1]["content"] = content


# 加载xml
def loadScaleXML(content):
    # 实例化xml处理对象
    handler = ScaleHandler()
    # 加载xml
    xml.sax.parseString(content, handler)
    return handler
