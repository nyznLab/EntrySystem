import xml.sax


class ScaleHandler(xml.sax.handler.ContentHandler):
    def __init__(self):
        super().__init__()
        self.scaleContent = {}
        self.currentQuestionIndex = -1
        self.CurrentData = ""

    # 元素开始事件处理
    def startElement(self, tag, attributes):
        self.CurrentData = tag
        if tag == "scale":
            self.scaleContent["title"] = attributes["title"]
            self.scaleContent["warn"] = attributes["warn"]
        if tag == "question":
            self.currentQuestionIndex = attributes["index"]
            self.scaleContent[attributes["index"]] = {
                "title": attributes["title"],
                "options": [],
            }
            if "rule" in attributes.keys():
                self.scaleContent[attributes["index"]]["rule"] = attributes["rule"]
        if tag == "option":
            self.scaleContent[self.currentQuestionIndex]["options"].append(
                {
                    "type": attributes["type"],
                    "name": attributes["name"],
                }
            )
            if "value" in attributes.keys():
                self.scaleContent[self.currentQuestionIndex]["options"][-1]["value"] = attributes["value"]

    # 内容事件处理
    def characters(self, content):
        if self.CurrentData == "option" and str(content).strip() != "":
            self.scaleContent[self.currentQuestionIndex]["options"][-1]["content"] = content


def loadScaleXML(content):
    handler = ScaleHandler()
    xml.sax.parseString(content, handler)
    return handler
