    def forward_chaining(rules, facts, goal):
        road = []
        while goal not in facts:
            rule_applied = False

            for rule in rules:
                if rule.flag1: continue #"bỏ qua, vì flag1 đã được cập nhật"
                if rule.flag2: continue # "bỏ qua, vì flag2 đã được cập nhật."
                if rule.right in facts:  # nếu vế phải đã được cm rồi
                    rule.flag2 = True
                    continue #"không áp dụng, vì rule.right nắm trong số các facts. Cập nhật flag2.\n" 
                    
                if rule được chứng minh là đúng:
                    rule_applied = True # vẫn còn luật để phê duyệt
                    rule.flag1 = True # cập nhật luật vào flag1
                    facts:= fact ∪ {rule.right} # thêm rule.right vào facts
                    road:= road ∪ {name(rule)} # thêm luật suy diễn được vào đường đi
                    break
                else: "Không được áp dụng, vì thiếu fact" 
                
            if not rule_applied: # nếu tất cả các luật đều đã sử dụng
                return False, road
        return True, road
    
    


    def do_backward_chaining( rules, target_facts, found_facts, current_goals, goal):
        
        if goal in target_facts: return True # đích mà có trong facts rồi thì chắc chắc yes
        if goal in current_goals:return False # vòng lặp vô hạn
        if goal in found_facts:return True # đích nằm trong các fact được tìm thấy

        results_count = len(road)# độ dài của đường đi

        for rule in rules:# lấy từng Rule(left, right)
            if rule.right == goal:# nếu right mà là goal
                is_satisfied = False

                for new_goal in rule.left:
                    current_goals =current_goals ∪ {goal}# thêm vào goal mới
                    
                    is_satisfied = do_backward_chaining(new_goal) # tiếp tục thực hiện quá trình suy diễn goal mới
                    if is_satisfied == False: return False
                    current_goals.pop() # xóa goal vừa làm đi
                    
                    if goal in found_facts : return True #nếu đích nằm trong facts suy diễn ra

                if is_satisfied: # hoàn thành thì cập nhật road
                    road= road ∪ (name(rule)) #thêm luật vào đường đi
                    found_facts = found_facts ∪ {rule.right} # thêm fact mới suy diễn được vào found_facts
                    return True

            while len(road) > results_count: road.pop()

        return False # không có luật nào suy diễn ra được