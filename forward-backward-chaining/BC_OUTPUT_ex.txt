PART 1. Data
  1) Productions
    R1: S01->D01
    R2: D01->D02
    R3: S02->S03
    R4: S06,S04->S07
    R5: S05,S02->S06
    R6: S01->S02

  2) Facts
    S01, S04.

  3) Goal
    S07.

PART 2. Execution
  1) Goal S07. Tìm thấy luật R4:S06,S04->S07. Các goals mới cần chứng mình là S06, S04.
  2) -Goal S06. Tìm thấy luật R5:S05,S02->S06. Các goals mới cần chứng mình là S05, S02.
  3) --Goal S05. Không có luật nào để suy diễn/ không có fact này ban đầu. Trả về thất bại.

PART 3. Results
  1) Goal S07 unreachable.
