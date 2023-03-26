class Rule:

    def __init__(self, left, right):
        self.left = left
        self.right = right
        self.flag1 = False
        self.flag2 = False

    def follows(self, facts): # tìm ra cái thiéu

        for fact in self.left:# lấy từng fact trong vế trái
            if fact not in facts: # nếu không thuộc list facts tổng thì trả về 
                return fact
        return None # trả về none khi mà vế trsi đủ điều kiện cho vế phải

    def __str__(self):
        return ",".join(self.left) + "->" + self.right


class ForwardChaining:

    def __init__(self, file_name):
        self.iteration = 0
        self.output = ""
        self.output_file_name = None

        self.output += "PART 1. Data\n"
        rules, facts, goal = self.read_data(file_name) # lấy luật , sự thật và mục tiêu
        self.print_data(rules, facts, goal)

        self.output += "PART 2. Execution\n"
        result, road = self.forward_chaining(rules, facts, goal)

        self.output += "PART 3. Results\n"
        self.print_results(result, road, goal)

        self.write_output(file_name)
        print("Result saved in file: %s." % self.output_file_name)

    def forward_chaining(self, rules, facts, goal):
        ir = len(facts)
        iteration = 0
        road = []

        # while goal not in facts: # khi mục tiêu chưa nằm trong facts tìm thấy
        while 1:
            rule_applied = False
            iteration += 1
            self.output += "%i".rjust(4, " ") % iteration + " ITERATION\n"

            for rule in rules:
                self.output += "    R%i:%s " % ((rules.index(rule) + 1), str(rule))

                if rule.flag1: # nếu luạt đã được cm rồi
                    self.output += "bỏ qua, vì flag1 đã được cập nhật.\n"
                    continue

                if rule.flag2: 
                    self.output += "bỏ qua, vì flag2 đã được cập nhật.\n"
                    continue

                if rule.right in facts:# nếu vế phải đã được cm rồi
                    self.output += "không áp dụng, vì %s nắm trong số các facts. Cập nhật flag2.\n" % rule.right
                    rule.flag2 = True
                    continue

                missing = rule.follows(facts) # tìm xem là có fact nào thiếu để kết luận luật đúng hay không 

                if missing is None:
                    rule_applied = True
                    rule.flag1 = True
                    facts.append(rule.right)
                    road.append("R" + str(rules.index(rule) + 1))
                    self.output += "được áp dụng. Cập nhật flag1. Facts %s suy ra %s.\n" % (
                        ", ".join(facts[:ir]), ", ".join(facts[ir:]))
                    break
                else: # do vế trái thiếu mất fact
                    self.output += "Không được áp dụng, vì thiếu fact: %s\n" % missing
            self.output += "\n"

            if not rule_applied:
                print(facts)
                print("Đường đi : ",road)
                return False, road# ban đầu là []

        return True, road

    def read_data(self, file_name):
        rules = []
        facts = []
        goal = None

        file = open(file_name, "r")
        read_state = 0

        for line in file:
            line = line.replace("\n", "")

            if line == "":
                read_state += 1
                continue
            if line[0] == '#':
                continue

            line = line.split(" ")

            if read_state == 0:
                right = line[0]
                left = line[1:]
                rules.append(Rule(left, right))

            if read_state == 1:
                facts = line

            if read_state == 2:
                goal = line[0]

            if read_state > 2:
                self.output += "Incorrect data file."
                return [], [], None

        return rules, facts, goal

    def print_data(self, rules, facts, goal):

        self.output += "  1) Productions\n"
        for rule in rules:
            self.output += "    R%i: %s\n" % (rules.index(rule) + 1, str(rule))
        self.output += "\n  2) Facts %s.\n" % ", ".join(facts)
        self.output += "\n  3) Goal %s\n\n" % goal

    def print_results(self, result, road, goal):

        if result:
            if len(road) == 0:
                self.output += "  1) Goal %s among facts.\n" % goal
                self.output += "  2) Empty road.\n"
            else:
                self.output += "  1) Goal %s derived.\n" % goal
                self.output += "  2) Road: %s.\n" % ", ".join(road)
        else:
            self.output += "  1) Goal %s unreachable.\n" % goal
            self.output += "  2) Đường đi suy diễn được là:%s"  %", ".join(road) #new

    def write_output(self, file_name):
        self.output_file_name = "FC_OUTPUT_%s.txt" % file_name.replace("/", ".")
        file = open(self.output_file_name, "w", encoding='utf8')
        file.write(self.output)
