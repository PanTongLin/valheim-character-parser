import struct
from enum import Enum

class Biome(Enum):
    none = 0
    Meadows = 1
    Swamp = 2
    Mountain = 4
    BlackForest = 8
    Plains = 16
    AshLands = 32
    DeepNorth = 64
    Ocean = 256
    Mistlands = 512
    BiomesMax = 513

class Skill(Enum):
    none = 0
    Swords = 1
    Knives = 2
    Clubs = 3
    Polearms = 4
    Spears = 5
    Blocking = 6
    Axes = 7
    Bows = 8
    FireMagic = 9
    FrostMagic = 10
    Unarmed = 11
    Pickaxes = 12
    WoodCutting = 13
    Jump = 100
    Sneak = 101
    Run = 102
    Swim = 103
    All = 999

class character:
    def __init__(self, file_path):
        self.load(file_path)
    
    def load(self, file_path):
        def read_bool(file):
            data = file.read(1)
            data = struct.unpack('?', data)[0]
            return False if data==0 else True
        def read_uchar(file):
            data = file.read(1)
            data = struct.unpack('B', data)[0]
            return data
        def read_int32(file):
            data = file.read(4)
            data = struct.unpack('<i', data)[0]
            return data
        def read_int64(file):
            data = file.read(8)
            data = struct.unpack('<q', data)[0]
            return data
        def read_float(file):
            data = file.read(4)
            data = struct.unpack('<f', data)[0]
            return data
        def read_str(file):
            data_len = read_uchar(file)
            data = file.read(data_len)
            data = struct.unpack(str(data_len)+'s', data)[0]
            return data

        with open(file_path, 'rb') as c_file:
            self.file_size = read_int32(c_file) # needs to be recalculated in case any string changes
            self.character_ver = read_int32(c_file)            
            self.kills = read_int32(c_file)
            self.deaths = read_int32(c_file)
            self.crafts = read_int32(c_file)
            self.builds = read_int32(c_file)

            self.num_worlds = read_int32(c_file)
            self.worlds = []
            for i in range(self.num_worlds):
                world = {}
                world['world_id'] = read_int64(c_file)
                world['has_custom_spawn_point'] = read_bool(c_file)
                world['spawn_point'] = (read_float(c_file), read_float(c_file), read_float(c_file))
                world['has_logout_point'] = read_bool(c_file)
                world['logout_point'] = (read_float(c_file), read_float(c_file), read_float(c_file))
                world['has_death_point'] = read_bool(c_file)
                world['death_point'] = (read_float(c_file), read_float(c_file), read_float(c_file))
                world['home_point'] = (read_float(c_file), read_float(c_file), read_float(c_file))

                world['has_map_data'] = read_bool(c_file)
                if world['has_map_data']:
                    world['map_data_len'] = read_int32(c_file)
                    world['map_data'] = c_file.read(world['map_data_len'])

                self.worlds.append(world)
            
            self.name = read_str(c_file)
            self.id = read_int64(c_file)
            self.start_seed = read_str(c_file)

            self.is_not_new = read_bool(c_file) # not sure
            if not self.is_not_new:
                c_file.close()
                return

            self.data_len = read_int32(c_file) # needs to be recalculated in case any string changes
            self.data_version = read_int32(c_file)

            self.max_hp = read_float(c_file)
            self.hp = read_float(c_file)
            self.stamina = read_float(c_file)
            self.is_first_spawn = read_bool(c_file)
            self.time_since_death = read_float(c_file)
            self.guardian_power = read_str(c_file)
            self.guardian_power_cd = read_float(c_file)

            self.inventory_ver = read_int32(c_file)
            self.num_items = read_int32(c_file)
            self.inventory = []
            for i in range(self.num_items):
                item = {}
                item['name'] = read_str(c_file)
                item['stack'] = read_int32(c_file)
                item['durability'] = read_float(c_file)
                item['pos'] = (read_int32(c_file), read_int32(c_file))
                item['equipped'] = read_bool(c_file)
                item['quality'] = read_int32(c_file)
                item['variant'] = read_int32(c_file)
                item['crafter_id'] = read_int64(c_file)
                item['crafter_name'] = read_str(c_file)

                self.inventory.append(item)

            self.num_recipes = read_int32(c_file)
            self.recipes = []
            for i in range(self.num_recipes):
                self.recipes.append(read_str(c_file))

            self.num_stations = read_int32(c_file)
            self.stations = []
            for i in range(self.num_stations):
                self.stations.append((read_str(c_file), read_int32(c_file)))

            self.num_known_materials = read_int32(c_file)
            self.known_materials = []
            for i in range(self.num_known_materials):
                self.known_materials.append(read_str(c_file))

            self.num_shown_tutorials = read_int32(c_file)
            self.shown_tutorials = []
            for i in range(self.num_shown_tutorials):
                self.shown_tutorials.append(read_str(c_file))

            self.num_uniques = read_int32(c_file)
            self.uniques = []
            for i in range(self.num_uniques):
                self.uniques.append(read_str(c_file))

            self.num_trophies = read_int32(c_file)
            self.trophies = []
            for i in range(self.num_trophies):
                self.trophies.append(read_str(c_file))

            self.num_biomes = read_int32(c_file)
            self.biomes = []
            for i in range(self.num_biomes):
                self.biomes.append(read_int32(c_file))

            self.num_texts = read_int32(c_file)
            self.texts = []
            for i in range(self.num_texts):
                self.texts.append((read_str(c_file), read_str(c_file)))

            self.beard = read_str(c_file)
            self.hair = read_str(c_file)
            self.skin_color = (read_float(c_file), read_float(c_file), read_float(c_file))
            self.hair_color = (read_float(c_file), read_float(c_file), read_float(c_file))
            self.model = read_int32(c_file)

            self.num_consumed_food = read_int32(c_file)
            self.consumed_food = []
            for i in range(self.num_consumed_food):
                food = {}
                food['name'] = read_str(c_file)
                food['hp_left'] = read_float(c_file)
                food['stamina_left'] = read_float(c_file)

                self.consumed_food.append(food)

            self.skill_ver = read_int32(c_file)
            self.num_skills = read_int32(c_file)
            self.skills = []
            for i in range(self.num_skills):
                skill = {}
                skill['name'] = read_int32(c_file)
                skill['level'] = read_float(c_file)
                skill['partial'] = read_float(c_file) # ??

                self.skills.append(skill)

            self.something = []
            while True:
                chunk = c_file.read(4)
                if chunk == b'':
                    break
                self.something.append(chunk)

            c_file.close()

    def save(self, file_path):
        def write_bool(file, data):
            data = struct.pack('?', data)
            file.write(data)            
        def write_uchar(file, data):
            data = struct.pack('B', data)
            file.write(data)
        def write_int32(file, data):
            data = struct.pack('<i', data)
            file.write(data)
        def write_int64(file, data):
            data = struct.pack('<q', data)
            file.write(data)
        def write_float(file, data):
            data = struct.pack('<f', data)
            file.write(data)
        def write_str(file, data):
            data_len = len(data)
            write_uchar(file, data_len)
            data = struct.pack(str(data_len)+'s', data)
            file.write(data)

        with open(file_path, 'wb') as c_file:
            write_int32(c_file, self.file_size)
            write_int32(c_file, self.character_ver)
            write_int32(c_file, self.kills)
            write_int32(c_file, self.deaths)
            write_int32(c_file, self.crafts)
            write_int32(c_file, self.builds)

            write_int32(c_file, self.num_worlds)
            for world in self.worlds:
                write_int64(c_file, world['world_id'])
                write_bool(c_file, world['has_custom_spawn_point'])
                write_float(c_file, world['spawn_point'][0])
                write_float(c_file, world['spawn_point'][1])
                write_float(c_file, world['spawn_point'][2])
                write_bool(c_file, world['has_logout_point'])
                write_float(c_file, world['logout_point'][0])
                write_float(c_file, world['logout_point'][1])
                write_float(c_file, world['logout_point'][2])
                write_bool(c_file, world['has_death_point'])
                write_float(c_file, world['death_point'][0])
                write_float(c_file, world['death_point'][1])
                write_float(c_file, world['death_point'][2])
                write_float(c_file, world['home_point'][0])
                write_float(c_file, world['home_point'][1])
                write_float(c_file, world['home_point'][2])
                
                write_bool(c_file, world['has_map_data'])
                if world['has_map_data']:
                    write_int32(c_file, world['map_data_len'])
                    c_file.write(world['map_data'])

            write_str(c_file, self.name)
            write_int64(c_file, self.id)
            write_str(c_file, self.start_seed)

            write_bool(c_file, self.is_not_new)
            if not self.is_not_new:
                c_file.close()
                return

            write_int32(c_file, self.data_len)
            write_int32(c_file, self.data_version)

            write_float(c_file, self.max_hp)
            write_float(c_file, self.hp)
            write_float(c_file, self.stamina)
            write_bool(c_file, self.is_first_spawn)
            write_float(c_file, self.time_since_death)
            write_str(c_file, self.guardian_power)
            write_float(c_file, self.guardian_power_cd)

            write_int32(c_file, self.inventory_ver)
            write_int32(c_file, self.num_items)
            for item in self.inventory:
                write_str(c_file, item['name'])
                write_int32(c_file, item['stack'])
                write_float(c_file, item['durability'])
                write_int32(c_file, item['pos'][0])
                write_int32(c_file, item['pos'][1])
                write_bool(c_file, item['equipped'])
                write_int32(c_file, item['quality'])
                write_int32(c_file, item['variant'])
                write_int64(c_file, item['crafter_id'])
                write_str(c_file, item['crafter_name'])

            write_int32(c_file, self.num_recipes)
            for recipe in self.recipes:
                write_str(c_file, recipe)

            write_int32(c_file, self.num_stations)
            for station in self.stations:
                write_str(c_file, station[0])
                write_int32(c_file, station[1])

            write_int32(c_file, self.num_known_materials)
            for known_material in self.known_materials:
                write_str(c_file, known_material)

            write_int32(c_file, self.num_shown_tutorials)
            for shown_tutorial in self.shown_tutorials:
                write_str(c_file, shown_tutorial)

            write_int32(c_file, self.num_uniques)
            for unique in self.uniques:
                write_str(c_file, unique)

            write_int32(c_file, self.num_trophies)
            for trophie in self.trophies:
                write_str(c_file, trophie)

            write_int32(c_file, self.num_biomes)
            for biome in self.biomes:
                write_int32(c_file, biome)

            write_int32(c_file, self.num_texts)
            for text in self.texts:
                write_str(c_file, text[0])
                write_str(c_file, text[1])

            write_str(c_file, self.beard)
            write_str(c_file, self.hair)
            write_float(c_file, self.skin_color[0])
            write_float(c_file, self.skin_color[1])
            write_float(c_file, self.skin_color[2])
            write_float(c_file, self.hair_color[0])
            write_float(c_file, self.hair_color[1])
            write_float(c_file, self.hair_color[2])
            write_int32(c_file, self.model)

            write_int32(c_file, self.num_consumed_food)
            for food in self.consumed_food:
                write_str(c_file, food['name'])
                write_float(c_file, food['hp_left'])
                write_float(c_file, food['stamina_left'])

            write_int32(c_file, self.skill_ver)
            write_int32(c_file, self.num_skills)
            for skill in self.skills:
                write_int32(c_file, skill['name'])
                write_float(c_file, skill['level'])
                write_float(c_file, skill['partial']) # ??

            for chunk in self.something:
                c_file.write(chunk)

            c_file.close()

    def __str__(self):
        char_str = ''
        char_str += 'character version : ' + str(self.character_ver) + '\n'
        char_str += 'kills : ' + str(self.kills) + '\n'
        char_str += 'deaths : ' + str(self.deaths) + '\n'
        char_str += 'crafts : ' + str(self.crafts) + '\n'
        char_str += 'builds : ' + str(self.crafts) + '\n'

        char_str += 'number of worlds : ' + str(self.num_worlds) + '\n'
        for i in range(self.num_worlds):
            char_str += '   %d: '%(i) + '\n'
            char_str += '   world id : ' + str(self.worlds[i]['world_id']) + '\n'
            char_str += '   has custom spawn point : ' + str(self.worlds[i]['has_custom_spawn_point']) + '\n'
            if(self.worlds[i]['has_custom_spawn_point']):
                char_str += '   spawn point : ' + str(self.worlds[i]['spawn_point']) + '\n'
            char_str += '   has logout point : ' + str(self.worlds[i]['has_logout_point']) + '\n'
            if(self.worlds[i]['has_logout_point']):
                char_str += '   logout point : ' + str(self.worlds[i]['logout_point']) + '\n'
            char_str += '   has death point : ' + str(self.worlds[i]['has_death_point']) + '\n'
            if(self.worlds[i]['has_death_point']):
                char_str += '   death point : ' + str(self.worlds[i]['death_point']) + '\n'
            char_str += '   home point : ' + str(self.worlds[i]['home_point']) + '\n'
            char_str += '   has map data : ' + str(self.worlds[i]['has_map_data']) + '\n'
            char_str += '   map data length : ' + str(self.worlds[i]['map_data_len']) + '\n'
            
            char_str += '----------------------------------------\n'

        char_str += 'name : ' + self.name.decode('utf-8') + '\n'
        char_str += 'ID : ' + str(self.id) + '\n'
        char_str += 'start seed : ' + self.start_seed.decode('utf-8') + '\n'
        char_str += 'is not new : ' + str(self.is_not_new) + '\n'
        char_str += 'data length : ' + str(self.data_len) + '\n'
        char_str += 'data version : ' + str(self.data_version) + '\n'

        char_str += 'max hp : ' + str(self.max_hp) + '\n'
        char_str += 'hp : ' + str(self.hp) + '\n'
        char_str += 'stamina : ' + str(self.stamina) + '\n'
        char_str += 'is first spawn : ' + str(self.is_first_spawn) + '\n'
        char_str += 'time since death : ' + str(self.time_since_death) + '\n'
        char_str += 'guardian power : ' + self.guardian_power.decode('utf-8') + '\n'
        char_str += 'guardian power cooldown : ' + str(self.guardian_power_cd) + '\n'

        char_str += 'number of items : ' + str(self.num_items) + '\n'
        char_str += 'number of recipes : ' + str(self.num_recipes) + '\n'
        char_str += 'number of stations : ' + str(self.num_stations) + '\n'
        char_str += 'number of known materials : ' + str(self.num_known_materials) + '\n'
        char_str += 'number of shown tutorials : ' + str(self.num_shown_tutorials) + '\n'
        char_str += 'number of uniques : ' + str(self.num_uniques) + '\n'
        char_str += 'number of trophies : ' + str(self.num_trophies) + '\n'
        char_str += 'number of biomes : ' + str(self.num_biomes) + '\n'
        char_str += 'number of texts : ' + str(self.num_texts) + '\n'

        char_str += 'beard : ' + self.beard.decode('utf-8') + '\n'
        char_str += 'hair : ' + self.hair.decode('utf-8') + '\n'
        char_str += 'skin color : ' + str(self.skin_color) + '\n'
        char_str += 'hair color : ' + str(self.hair_color) + '\n'

        char_str += 'number of consumed food : ' + str(self.num_consumed_food) + '\n'

        char_str += 'number of skills : ' + str(self.num_skills) + '\n'

        return char_str

    def show_inventory(self):
        for item in self.inventory:
            '''
            item['name'] = read_str(c_file)
                item['stack'] = read_int32(c_file)
                item['durability'] = read_float(c_file)
                item['pos'] = (read_int32(c_file), read_int32(c_file))
                item['equipped'] = read_bool(c_file)
                item['quality'] = read_int32(c_file)
                item['variant'] = read_int32(c_file)
                item['crafter_id'] = read_int64(c_file)
                item['crafter_name'] = read_str(c_file)
                '''
            print('name :', item['name'].decode('utf-8'))
            print('stack :', str(item['stack']))
            print('durability :', str(item['durability']))
            print('position :', str(item['pos']))
            print('equipped :', str(item['equipped']))
            print('quality :', str(item['quality']))
            print('variant :', str(item['variant']))
            print('crafter_id :', str(item['crafter_id']))
            print('crafter_name :', item['crafter_name'].decode('utf-8'))
            print('----------------------------------------')

    def show_recipes(self):
        for recipe in self.recipes:
            print(recipe.decode('utf-8'))

    def show_stations(self):
        for station in self.stations:
            print(station[0].decode('utf-8'), str(station[1]))
    
    def show_known_materials(self):
        for known_material in self.known_materials:
            print(known_material.decode('utf-8'))

    def show_shown_tutorials(self):
        for shown_tutorial in self.shown_tutorials:
            print(shown_tutorial.decode('utf-8'))

    def show_uniques(self):
        for unique in self.uniques:
            print(unique.decode('utf-8'))

    def show_trophies(self):
        for trophie in self.trophies:
            print(trophie.decode('utf-8'))

    def show_biomes(self):
        for biome in self.biomes:
            print(Biome(biome))

    def show_texts(self):
        for text in self.texts:
            print(text[0].decode('utf-8'), text[1].decode('utf-8'))

    def show_consumed_food(self):
        for food in self.consumed_food:
            print(food['name'].decode('utf-8'))
            print('    hp left :', str(food['hp_left']))
            print('    stamina left :', str(food['stamina_left']))

    def show_skills(self):
        for skill in self.skills:
            print(Skill(skill['name']))
            print('    level :', str(skill['level']))
            print('    partial :', str(skill['partial']))