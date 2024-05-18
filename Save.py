from Player import*
import os
import json
class SaveFile:
    def __init__(self):
        pass
    def __init__(self, maze_toString: list[list[str]], player: Player):
        self.component = {
            'player.name': player.name,
            'player.grid_pos': player.grid_pos,
            'player.visual_pos': player.visual_pos,
            "level": "Easy",
            "mode" : "Manual",
            "score": 0,
            'maze_toString': maze_toString,
        }
    def run_save(self, file_name: str):
        with open('SaveFile/' + file_name + '.json', "w") as file:
            json.dump(self.component, file, indent=4)
            
    
def read_file( file_name:str):
    with open('SaveFile/' + file_name + '.json', "r") as file:
        data = json.load(file)
        # print(data)
        return data

def leader_board() -> list[str]:
    """_summary_

    Returns:
        list[str]: name of player list
    """
    file_list = os.listdir('SaveFile')
    leader_list = []
    leader_dict = {}
    for file in file_list:
        with open('SaveFile/' + file, 'r') as f_json:
            data = json.load(f_json)
            name, score, level = data['player.name'] , data['score'], data['level']
            if level not in leader_dict:
                leader_dict[level] = [(score, name)]
            else:
                leader_dict[level].append((score, name))
    
    for key_name in leader_dict.keys():
        leader_dict[key_name] = sorted(leader_dict[key_name], reverse = True)
    
    return leader_dict

def liet_ke():
    for file in os.listdir('SaveFile'):
        print(file)

def check_file(file_name):
    file_list = os.listdir('SaveFile')
    for i in range(len(file_list)):
        file_list[i] = file_list[i][:-5]
    return file_name in file_list

print(check_file('test1'))
print(leader_board())