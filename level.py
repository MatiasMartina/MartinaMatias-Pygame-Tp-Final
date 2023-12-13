from models.constantes import DEBUG_LEVEL, actual_level
import csv
class Level():
    def __init__(self, level):
        self.actual_level = level
        if DEBUG_LEVEL:
            print(f"player.level (inits) {level}")
        self.level = level
        
        pass


#Agregar un parámetro
    def load_level(self):
        filename = f'level{self.actual_level}.csv'
        if DEBUG_LEVEL:
            print(f'self.level: (Tras inicio de la carga){self.level}')
        with open(filename, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.reader(csv_file)
            world_data = []
            for row_tiles in csv_reader:
                individual_tiles = []
                for value in row_tiles:
                    try:
                        int_value = int(value)
                        individual_tiles.append(int_value)
                    except ValueError:
                        print(f"Error: No se pudo convertir a entero - Valor: {value}")
                        # Puedes decidir cómo manejar el valor que no se puede convertir, por ejemplo, asignar un valor predeterminado o simplemente ignorarlo
                        individual_tiles.append(0)
                world_data.append(individual_tiles)
            return world_data
        