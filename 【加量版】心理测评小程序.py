import tkinter as tk
from tkinter import messagebox
import tkinter.font as tkFont


class PsychologicalTestApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("心理测评小程序")
        self.root.geometry("600x500")
        self.root.configure(bg='#f0f0f0')  # 窗口背景颜色
        self.current_test = None  # 存储当前正在进行的测试
        self.answers = []  # 存储用户的答案
        self.current_question_index = 0  # 当前问题的索引
        self.test_choices = {
            "气质类型测量": (self.temperament_questions, self.calculate_temperament_result),
            "职业性格测量": (self.career_personality_questions, self.calculate_career_personality_result),
            "霍兰德职业兴趣量表": (self.holland_questions, self.calculate_holland_result)
        }
        # 自定义字体
        self.title_font = tkFont.Font(family="Times New Roman", size=24)
        self.button_font = tkFont.Font(family="Times New Roman", size=24)
        self.question_font = tkFont.Font(family="Times New Roman", size=24)
        self.option_font = tkFont.Font(family="Times New Roman", size=12)
        self.create_widgets()

    def create_widgets(self):
        # 标题标签
        title_label = tk.Label(self.root, text="心理测评小程序", font=self.title_font, bg='#f0f0f0')
        title_label.pack(pady=20)

        # 测试选择按钮
        button_frame = tk.Frame(self.root, bg='#f0f0f0')
        button_frame.pack(pady=20)
        for test_name in self.test_choices.keys():
            button = tk.Button(button_frame, text=test_name, command=lambda name=test_name: self.start_test(name),
                             font=self.button_font, bg='#4CAF50', fg='white', padx=20, pady=10, borderwidth=0, relief=tk.RAISED)
            button.pack(pady=10, fill=tk.X)

    def start_test(self, test_name):
        self.current_test = self.test_choices[test_name]
        self.answers = []
        self.current_question_index = 0
        self.show_question()

    def show_question(self):
        if self.current_question_index < len(self.current_test[0]):
            question = self.current_test[0][self.current_question_index][0]
            options = self.current_test[0][self.current_question_index][1]

            # 清除之前的问题和选项
            for widget in self.root.winfo_children():
                widget.destroy()

            # 显示问题和选项
            question_frame = tk.Frame(self.root, bg='#f0f0f0')
            question_frame.pack(pady=20)
            question_label = tk.Label(question_frame, text=question, font=self.question_font, bg='#f0f0f0')
            question_label.pack(pady=10)
            for option in options:
                option_button = tk.Button(question_frame, text=option[0],
                                       command=lambda o=option[1]: self.save_answer(o),
                                       font=self.option_font, bg='#e0e0e0', padx=20, pady=5, borderwidth=0, relief=tk.RAISED)
                option_button.pack(pady=5, fill=tk.X)
        else:
            self.current_test[1]()  # 调用相应的结果计算函数

    def save_answer(self, answer):
        self.answers.append(answer)
        self.current_question_index += 1
        self.show_question()

    def calculate_temperament_result(self):
        scores = {"胆汁质": 0, "多血质": 0, "粘液质": 0, "抑郁质": 0}
        for answer in self.answers:
            if answer == "A":
                scores["胆汁质"] += 1
            elif answer == "B":
                scores["多血质"] += 1
            elif answer == "C":
                scores["粘液质"] += 1
            elif answer == "D":
                scores["抑郁质"] += 1
        result = max(scores, key=scores.get)
        messagebox.showinfo("气质类型测量结果", f"你的气质类型是：{result}")
        self.show_main_menu()

    def calculate_career_personality_result(self):
        a_count = self.answers.count("A")
        b_count = self.answers.count("B")
        c_count = self.answers.count("C")
        result = ""
        if a_count > b_count and a_count > c_count:
            result = "你是一个具有开拓精神、独立自信的人，适合从事具有挑战性的工作，如销售、创业、项目管理等。"
        elif b_count > a_count and b_count > c_count:
            result = "你是一个注重细节、善于分析的人，适合从事研究、数据分析、财务等工作。"
        elif c_count > a_count and c_count > b_count:
            result = "你是一个注重团队合作、善于沟通的人，适合从事人力资源、客服、行政等工作。"
        else:
            result = "你的性格较为平衡，能够适应多种工作类型，可以根据自己的兴趣和技能选择职业。"
        messagebox.showinfo("职业性格测量结果", result)
        self.show_main_menu()

    def calculate_holland_result(self):
        scores = {"R": 0, "I": 0, "A": 0, "S": 0, "E": 0, "C": 0}
        for answer in self.answers:
            scores[answer] += 1
        result = max(scores, key=scores.get)
        holland_codes = {
            "R": "现实型，适合从事机械、农业、户外等工作。",
            "I": "研究型，适合从事科研、技术、学术等工作。",
            "A": "艺术型，适合从事艺术、设计、音乐等工作。",
            "S": "社会型，适合从事教育、服务、医疗等工作。",
            "E": "企业型，适合从事管理、销售、领导等工作。",
            "C": "常规型，适合从事财务、行政、秘书等工作。"
        }
        messagebox.showinfo("霍兰德职业兴趣量表结果", f"你的霍兰德代码是：{result}\n{holland_codes[result]}")
        self.show_main_menu()

    def show_main_menu(self):
        for widget in self.root.winfo_children():
            widget.destroy()
        self.create_widgets()

    # 气质类型测量的问题和选项
    temperament_questions = [
        ("当你遇到令你生气的事情时，你会：", [("A. 立刻爆发，难以控制情绪", "A"),
                                        ("B. 很快就会忘记，继续投入新的事情", "B"),
                                        ("C. 冷静对待，理智处理", "C"),
                                        ("D. 暗自生闷气，情绪低落", "D")]),
        ("在社交场合中，你通常：", [("A. 主导话题，充满活力", "A"),
                                ("B. 轻松愉快，喜欢交流", "B"),
                                ("C. 安静倾听，偶尔参与", "C"),
                                ("D. 感到紧张，不太自在", "D")]),
        ("当你和朋友在选择聚会地点产生分歧时，你会：", [("A. 坚持自己的选择，绝不妥协", "A"),
                                                ("B. 听从朋友的意见，心里有些不情愿", "B"),
                                                ("C. 与朋友共同商量，寻找一个双方都满意的折衷方案", "C"),
                                                ("D. 觉得很生气，直接拒绝参加聚会", "D")]),
        ("当你在工作中被领导批评，即便你认为自己没有错时，你会：", [("A. 当场与领导顶嘴，为自己辩解", "A"),
                                                            ("B. 表面接受批评，但内心还是很不服气", "B"),
                                                            ("C. 先冷静听完领导的话，之后找合适的时机再沟通解释", "C"),
                                                            ("D. 觉得委屈，一整天工作效率都很低", "D")]),
        ("当你精心准备了很久的计划被意外打乱时，你会：", [("A. 非常懊恼，对打乱计划的人或事大发雷霆", "A"),
                                                    ("B. 虽然有些不开心，但很快就接受现实，不再去想", "B"),
                                                    ("C. 迅速调整心态，重新规划方案", "C"),
                                                    ("D. 陷入消极情绪，抱怨运气不好", "D")]),    
    ]

    # 职业性格测量的问题和选项
    career_personality_questions = [
            ("当面对工作中的困难时，你会：", [("A. 大胆尝试新方法，不怕失败", "A"), 
                                        ("B. 仔细分析问题，寻找最佳方案", "B"), 
                                        ("C. 寻求同事或上级的帮助", "C")]),
            ("在团队项目中，你更倾向于：", [("A. 领导团队，分配任务", "A"), 
                                        ("B. 遵循指示，完成分配的任务", "B"), 
                                        ("C. 协调团队成员之间的关系", "C")]),
            ("在做出重要决策时，你通常：", [("A. 依赖直觉", "A"), 
                                        ("B. 依赖逻辑和分析", "B"), 
                                        ("C. 寻求他人的意见", "C")]),
            ("面对紧急的截止日期，你倾向于：", [("A. 保持冷静，合理安排时间", "A"), 
                                            ("B. 感到压力，但仍然尽力而为", "B"), 
                                            ("C. 感到焦虑，可能需要额外支持", "C")]),
            ("在团队讨论中，你通常：", [("A. 主动发言，分享观点", "A"), 
                                    ("B. 倾听他人，然后谨慎发言", "B"), 
                                    ("C. 观察情况，很少发言", "C")])
        ]

    # 霍兰德职业兴趣量表的问题和选项
    holland_questions = [
    ("你更喜欢：", [("A. 修理电器或机器", "R"),
                  ("B. 做科学实验", "I"),
                  ("C. 绘画或演奏音乐", "A"),
                  ("D. 帮助他人解决问题", "S"),
                  ("E. 组织活动或领导团队", "E"),
                  ("F. 整理文件和数据", "C")]),
    ("对于工作环境，你更倾向于：", [("A. 户外或工厂", "R"),
                              ("B. 实验室或图书馆", "I"),
                              ("C. 艺术工作室", "A"),
                              ("D. 学校或社区中心", "S"),
                              ("E. 商务办公室", "E"),
                              ("F. 办公室或行政部门", "C")]),
    ("在工作中的压力应对方式上，你更倾向于：",[("A. 通过艺术创作来释放压力", "A"),
                                       ("B. 独自思考解决问题的方法", "I"),
                                       ("C. 专注于手头的具体任务来忘却压力", "R"),
                                       ("D. 与朋友或同事倾诉来缓解压力", "S"),
                                       ("E. 制定计划来掌控和消除压力源", "E"),
                                       ("F. 按部就班地处理事务来减轻压力", "C")]),
    ("在工作任务类型上，你更倾向于：", [("A. 设计服装或建筑", "A"),
                                ("B. 分析数据或研究理论", "I"),
                                ("C. 操作机械或维修设备", "R"),
                                ("D. 教导学生或培训员工", "S"),
                                ("E. 管理项目或制定策略", "E"),
                                ("F. 记录账目或处理财务", "C")]),
    ("对于工作中的社交互动，你更倾向于：",[("A. 独立工作，很少与他人交流", "R"),
                                  ("B. 与少数专业人士交流想法", "I"),
                                  ("C. 在团队中协作完成创意项目", "A"),
                                  ("D. 频繁与客户或公众沟通", "S"),
                                  ("E. 领导和指挥团队成员", "E"),
                                  ("F. 与同事进行日常事务性交流", "C")])
    ]

if __name__ == "__main__":
    app = PsychologicalTestApp()
    app.root.mainloop()