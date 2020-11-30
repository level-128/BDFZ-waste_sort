from .config.config_library import config
import json


my_category_dir: str = config["garbage_category_file_dir"]

file = open(my_category_dir, "r", encoding="utf-8")
my_category = json.loads(file.read())
file.close()


def save_category():
    file_ = open(my_category_dir, "w+", encoding="utf-8")
    file_.write(json.dumps(my_category))
    file_.close()


def classify_garbage(image_tagging_result: list):
    for item in image_tagging_result:
        for category in my_category:
            if item[1] in my_category[category]:
                return category
        if config["is_record_none_category"]:
            config["none_category"].append(item[1])
    if config["learn_mode"]:
        return learn(image_tagging_result)
    else:
        return "识别失败"


def learn(image_tagging_result: list):
    print("识别失败")
    print(f"它可能是 {[_[1] for _ in image_tagging_result]} 其中一个，请问它是第几个？")
    while True:
        name = input(">> ")
        if name == "无":
            return "识别失败"
        else:
            try:
                count = (int(name) - 1)
                assert count >= 0
                item_name = [_[1] for _ in image_tagging_result][count]
                break
            except IndexError:
                print("输入无效")

    print("请问这个属于 可回收垃圾 有害垃圾 厨余垃圾 其他垃圾 中的第几个？")
    while True:
        name = input(">> ")
        try:
            count = (int(name) - 1)
            assert count >= 0
            item_category = ['可回收垃圾', '有害垃圾', '厨余垃圾', '其他垃圾'][count]
            my_category[item_category].append(item_name)
            save_category()
            break
        except IndexError:
            print("输入无效")
    return item_category
