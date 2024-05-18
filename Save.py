from Player import*
import os
import json
class SaveFile:
    def __init__(self):
        pass
    def __init__(self, maze_toString: list[list[str]], player: Player):
        self.player = player
        self.component = {
            'player.name': player.name,
            'player.grid_pos': player.grid_pos,
            'player.visual_pos': player.visual_pos,
            "level": "Easy",
            "mode" : "Manual",
            "score": player.score,
            'maze_toString': maze_toString,
        }
    def run_save(self, file_name: str):
        with open('SaveFile/' + file_name + '.json', "w") as file:
            json.dump(self.component, file, indent=4)
    
def read_file( file_name:str):
    """_summary_

    Args:
        file_name (str): name of file open

    Returns:
        _type_: dictionary
    """
    with open('SaveFile/' + file_name + '.json', "r") as file:
        data = json.load(file)
        # print(data)
        return data


def update_leader_board(player: Player, score, level):
    with open('leader_board.json', 'r') as f_json:
        data = json.load(f_json)

    if level not in data:
        data[level] = {player.name: score}
    else:
        if player.name not in data[level]:
            data[level][player.name] = score
        else:
            data[level][player.name] = max(score, data[level][player.name])
    
    for key in data.keys():
        data[key] = dict(sorted(data[key].items(), key=lambda x: (-x[1])))
        
    with open('leader_board.json', 'w') as f_json:
        json.dump(data, f_json, indent=4)
   
def get_leader_board():
    with open('leader_board.json', 'r') as f_json:
        data = json.load(f_json)
    for key in data.keys():
        data[key] = dict(sorted(data[key].items(), key=lambda x: (-x[1])))
    return data

def remove_file(file_name):
    if os.path.exists('SaveFile/' + file_name + '.json'):
        os.remove('SaveFile/' + file_name + '.json')
        
def check_file(file_name):
    """_summary_

    Args:
        file_name (_type_): ten cua file dat khi save game

    Returns:
        True -> file name da ton tai phai dat file khac
        False -> file name chua ton tai -> dc phep dat file
    """
    file_list = os.listdir('SaveFile/')
    for i in range(len(file_list)):
        file_list[i] = file_list[i][:-5]
    #print(file_list)
    return file_name in file_list

def repath_file_win():
    """
    covert cac file o folder un win sang folder win
    nghia la cac file da choi het
    """
    file_list = os.listdir('SaveFile/')
    for i in range(len(file_list)):
        with open('SaveFile/' + file_list[i]) as f_json:
            data = json.load(f_json)
        if data['score'] != 0:
            os.rename("SaveFile/" + file_list[i][:-5] + ".json","SaveFile/" + file_list[i][:-5] + "_win.json")
    
    
# print(check_file('test1'))
# print(leader_board())
# repath_file_win()

print(get_leader_board())