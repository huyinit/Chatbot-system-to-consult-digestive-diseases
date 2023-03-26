from class_all import ConvertData
class Rule:
    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.flag1 = False
        self.flag2 = False
        # self.r=r

    def follows(self, facts):# facts là các triệu chứng đã có
        for fact in self.left: # cho từng luật ở vế trái
            if fact not in facts: # nếu như luật đó ko tồn tại trong facts ban đầu
                return fact # thì trả về cái luật đó
        return None

    def __str__(self):
        return "%s->%s" % (",".join(self.left), self.right)

class BackwardChaining:
    def __init__(self,rule,fact,goal,file_name):
        self.output = ""
        self.output_file_name = None
        self.iteration = 0
        self.road=None
        self.output += "PART 1. Dữ liệu\n"
        self.rules=self.read_rule(rule)
        self.target_facts=self.read_facts(fact)
        self.goal=goal
        # rule là 1 list các Rule(left, right) , facts là 1 dòng , goal là 1 ký tự
        self.print_data(self.rules, self.target_facts, self.goal)# in part1

        self.output += "PART 2. Suy diễn\n"
        result = self.do_backward_chaining(self.goal) # => true / false
        self.result1=result
        self.output += "\n" + "PART 3. Kết quả\n"
        self.print_result(result)

        self.write_output(file_name)
    def do_backward_chaining(self, goal, indent=""):# trả về giá trị true false caajp0 nhật cho result
        ls=0 # Biến điều kiện, nếu ls==0 thì không có luật nào phù hợp với goal và fact thì trả về false
        for rule in self.rules:
            # ls=0
            dk=1 #Biến điều kiện để dừng vòng lặp khi có triệu chứng không thuộc fact ban đầu
            
            if rule.right==goal:
                self.print_step(goal, indent, "Tìm thấy luật %s. Các goals mới cần chứng mình là %s." % ("R" + str(self.rules.index(rule) + 1) + ":" + str(rule), ", ".join(rule.left)))
                # print(f"rule {rule.left}")
                for f in range(len(rule.left)):
                    fact_guess=str(rule.left[f])
                    if fact_guess not in self.target_facts:
                        self.print_step(fact_guess, indent + '-', "Không có luật nào để suy diễn/không có triệu chứng này ban đầu. Trả về thất bại.")
                        dk=0
                        break
                    else:
                        self.print_step(fact_guess, indent +"-", "Cập nhật triệu chứng %s, bởi vì được tìm thấy trong tập triệu chứng gốc %s. Trả về thành công." % (
                                        fact_guess, ", ".join(self.target_facts)))

                        
                        # dk=1
                self.road="R" + str(self.rules.index(rule) + 1)
                
                if dk==1: #Kiểm tra nếu đúng hết các triệu chứng thì dừng vòng lặp
                    ls=1 #Kiểm tra xem có fact nào có trong tập luật ban đầu không
                    self.print_step(rule.right,indent+"==>","Đã được chứng minh, Trả về thành công")
                    break 
        if ls==0: #Nếu không có luật nào trả lời đùng theo fact thì dừng
            self.print_step(goal, indent, "Không có luật nào để suy diễn/không có triệu chứng này ban đầu. Trả về thất bại.")
            return False
        else:
            return True
    # def get_s_in_fact(self):

    def print_step(self, goal, indent, msg):#indent : dấu gạch ngang
        self.iteration += 1
        self.output += str(self.iteration).rjust(3, " ") + ") %sGoal %s. " % (indent, goal) + msg + "\n"

    def read_data(self, file_name):
        rules = []
        facts = []
        goal = None

        file = open(file_name, "r")
        read_state = 0

        for line in file:# lấy từng dòng
            line = line.replace("\n", "")
            if line == "":# kiểm tra dòng rỗng => phần sau chính là fact hoặc goal 
                read_state += 1
                continue
            line = line.split(" ") # ko rỗng thì chặt ra list

            if line[0] == '#': # dấu thăng thì bỏ qua
                continue

            if read_state == 0:
                right = line[0]# vế trái cùng là đích
                left = line[1:]# vế phải là các luật suy diễn
                # vd L A B thì ta hiểu là A+B => L
                rules.append(Rule(left, right)) # thêm luật đó vào mảng rules

            if read_state == 1:
                facts = line # đây là các triệu chứng thực tế đã gặp

            if read_state == 2:
                goal = line[0]

        return rules, facts, goal# rule là 1 list các Rule(left, right), facts là 1 dòng , goal là 1 ký tự
    def read_rule(self,rule):
        new_rule=[]
        id=0
        for i in rule:
            right=i[0]
            left=i[1:]
            # id+=1

            new_rule.append(Rule(left,right))
        # print(new_rule)
        return new_rule
    def read_facts(self,line):
        ad=[]
        for i in line:
            ad.append(i)
        return ad
    def print_data(self, rules, facts, goal):
        self.output += "  1) Tập luật\n"
        for rule in rules:
            self.output += "    R%i: %s\n" % (rules.index(rule) + 1, str(rule))
        self.output += "\n  2) Triệu chứng người dùng mắc phải\n    %s.\n\n" % ", ".join(facts)
        self.output += "  3) Bệnh nghi ngờ\n    %s.\n\n" % goal

    def print_result(self, result): # part 3
        if result is not False:

            if len(self.road) == 0:
                self.output += "  1) Goal %s được chứng minh.\n" % self.goal
                self.output += "  2) Empty road.\n"
            else:
                self.output += "  1) Goal %s được chứng minh.\n" % self.goal
                self.output += "  2) Road: %s.\n" % (self.road)
        else:
            self.output += "  1) Goal %s không được chứng minh.\n" % self.goal

    def write_output(self, file_name):
        self.output_file_name = "BC_OUTPUT_%s.txt" % file_name.replace("/", ".")
        file = open(self.output_file_name, "w", encoding='utf8')
        file.write(self.output)