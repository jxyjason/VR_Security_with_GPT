import os

import openai
import xml.etree.ElementTree as ET
import subprocess
import shutil
import time

openai.api_key = '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'
# openai.api_key = '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'
def ask_gpt(messages):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )
    # 解析回答
    answer = response.choices[0].message.content
    return answer

def decompilation(apk_name):
    command = "java -jar apktool_2.9.0.jar d " + apk_name + " -o app"
    # 运行命令行指令
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    # 获取命令行输出结果
    output, error = process.communicate()
    # 解码输出结果和错误信息
    # output = output.decode()
    # error = error.decode()
    # 返回输出结果和错误信息
    return output, error

def analyzeOneApk(apk_src,description):
    try:
        # 反编译apk，输出为app文件夹
        decompilation(apk_src)
        # 读取xml
        tree = ET.parse('app/AndroidManifest.xml')
        root = tree.getroot()
        xml_string = ET.tostring(root, encoding='utf-8').decode('utf-8')

        # # 读取游戏介绍（用于测试，现改为直接作为形式参数输入）
        # with open("description.txt", 'r', encoding='utf-8') as file:
        #     description = file.read()

        # 初始化messages
        messages = [
            {"role": "system", "content": "You are an assistant with clear and concise assistant"}
        ]

        # 提问xml文件
        question = "Analyze which permissions and features are used by the decompiled xml file below (only need permissions and features):\n"+xml_string
        messages.append({"role": "user", "content": question})
        answer = ask_gpt(messages)
        xmlPermissionAndFeature = answer
        # print(answer)
        # 附加回答信息
        # messages.append({"role": "assistant", "content": answer})
        # print("--------------------------------------------------\n")

        # # 提问游戏介绍
        # question = "Take a look at permissions and features that might be used for this game, as described below:\n"+description
        # messages.append({"role": "user", "content": question})
        # answer = ask_gpt(messages)
        # print(answer)
        # # 附加回答信息
        # messages.append({"role": "assistant", "content": answer})
        # print("--------------------------------------------------\n")

        for i in range(21):
            time.sleep(1)
            print("sleep:" + str(i + 1) + "s")

        # 重新开一个提问进行二阶提问，针对问题描述和已经提取好的xml文件
        messages = [
            {"role": "system", "content": "You are an assistant with clear and concise assistant"},
            # {"role": "system", "content": "You are an assistant with clear and concise assistant"},#input
            # {"role": "system", "content": "You are an assistant with clear and concise assistant"},
        ]

        # 提问哪些不该用
        question = "Based on the Permissions And Features and game description,  which sensitive permissions and features should not be requested (Simply answer the permissions and features mentioned in the question). \n" \
                   "** All you have to do is analyze what's below: **\n" \
                    "\n```\n"+xmlPermissionAndFeature+"\n```\n" \
                   "\ndescription:\n```\n" + description + "\n```\n" \
                   # \
                   # "\nAn Example:" \
                   # "\nIf the Permissions And Features are : \n```\n android.permission.ACCESS_NETWORK_STATE\nandroid.permission.ACCESS_FINE_LOCATION\nandroid.permission.CAMERA\nandroid.permission.RECORD_AUDIO、\n ```"\
                   # "\nAnd the description is :```在太空中，飞船突发意外，你需要几岁各式各样的陨石来通过不同挑战。需要和同伴一起攻克难关。```\n"\
                   # "According to the description this game does not need to be online and does not require location information, so your answer is:\n"\
                   # "```\nThe ACCESS_FINE_LOCATION and CAMERA is not required.\nBecause the description says that the game needs to be played with other players, then the RECORD_AUDIO is need.\n```"
        print(question)
        messages.append({"role": "user", "content": question})
        answer = ask_gpt(messages)
        print(answer)

        # 删除反编译文件夹
        shutil.rmtree("app")

        return answer,xml_string

    except Exception as e:
        if os.path.exists("app") and os.path.isdir("app"):
            shutil.rmtree("app")
        print(f"Error occurred: {str(e)}")

if __name__ == "__main__":

    apk_src = "D:\\ict\\My_Project\\Security\\reverse\\reverse_app\\gpt_app\\9月的晚餐_SepsDiner_8592_19.apk"
    description = "It is an online game. Sep’s Diner，这是一家由您担任主厨的新汉堡餐厅！它真的会成为镇上最好的汉堡吗？现在就看你了！一层又一层，您的体验将增加，美食客户的数量也会增加。他们很匆忙，所以在他们离开之前尽快满足他们！饥饿和不耐烦，他们不会让您犯错误…… 细心和精确，以获得最大的利润！包括全新的甜点餐厅Sep’s Donut！游戏特色：· 2间餐厅· 包括 3 种游戏模式：定时、轻松、多人· 每家餐厅包括 27 个级别（定时/休闲 12 个，多人游戏 3 个）· 最多 4 名玩家的多人合作游戏· 紧张刺激的关卡！· 身临其境的音频氛围· 不耐烦的客户用有趣的声音· 美丽的风景和彩灯· 逐级增加难度· 超过 30 种不同的汉堡食谱组合！· 煎饼、甜甜圈、华夫饼、纸杯蛋糕、冰淇淋和奶昔！"
    analyzeOneApk(apk_src,description)



