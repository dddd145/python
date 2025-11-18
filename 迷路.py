import random
import os
import sys

WIDTH = 15
HEIGHT = 11
WALL = '█'
PATH = ' '
PLAYER = 'P'
GOAL = 'G'
player_x, player_y = 1, 1
current_stage = 1
maze_map = []

# 迷路生成
def generate_maze_map():
  global maze_map
  # 初期化
  maze_map = [[WALL] * WIDTH for _ in range(HEIGHT)]
  visited = set()
  stack = [(1, 1)]

  # 迷路生成
  while stack:
    cx, cy = stack[-1]
    # 現在のセルを通路にする
    maze_map[cy][cx] = PATH
    visited.add((cx, cy))
    # 隣接セルのリストを作成
    neighbors = []
    for dx, dy in [(0, 2), (0, -2), (2, 0), (-2, 0)]:
      nx, ny = cx + dx, cy + dy
      # 範囲内かつ未訪問
      if 1 <= nx < WIDTH - 1 and 1 <= ny < HEIGHT - 1 and (nx, ny) not in visited:
        neighbors.append((nx, ny, dx, dy))
    if neighbors:
      # ランダムに次のセルを選択
      nx, ny, dx, dy = random.choice(neighbors)
      # 間の壁を通路にする
      maze_map[cy + dy // 2][cx + dx // 2] = PATH
      stack.append((nx, ny))
    else:
      stack.pop()

  # スタート位置
  global player_x, player_y
  player_x, player_y = 1, 1
  maze_map[1][1] = PLAYER

  # ゴール位置
  goal_x, goal_y = WIDTH - 2, HEIGHT - 2
  maze_map[goal_y][goal_x] = GOAL

# 処理系関数
def clear_screen():
  os.system('cls' if os.name == 'nt' else 'clear')

# 迷路描画
def draw_maze():
  clear_screen()
  print(f"--- 迷路ステージ {current_stage} ---")
  for row in maze_map:
    print("".join(row))
  print("------------------------")
  print("移動: w/a/s/d || q:終了")

# プレイヤー移動
def move_player(dx, dy):
  global player_x, player_y, current_stage
  new_x = player_x + dx
  new_y = player_y + dy
  # 範囲外
  if not (0 <= new_x < WIDTH and 0 <= new_y < HEIGHT):
    return
  target_cell = maze_map[new_y][new_x]
  # 壁
  if target_cell == WALL:
    return
  # ゴール
  elif target_cell == GOAL:
    print("\n次のステージへ進みます！")
    maze_map[player_y][player_x] = PATH
    current_stage += 1
    generate_maze_map()
    return
  elif target_cell == PATH:
    maze_map[player_y][player_x] = PATH
    player_x = new_x
    player_y = new_y
    maze_map[player_y][player_x] = PLAYER
    return

# メインループ
def main():
  generate_maze_map()
  while True:
    draw_maze()
    command = input("コマンド > ").lower()
    dx, dy = 0, 0
    if command == 'q':
      print("\nゲームを終了します。")
      sys.exit()
    elif command == 'w':
      dy = -1
    elif command == 's':
      dy = 1
    elif command == 'a':
      dx = -1
    elif command == 'd':
      dx = 1
    else:
      continue
    move_player(dx, dy)

if __name__ == '__main__':
  main()
