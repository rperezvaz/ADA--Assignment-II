import numpy as np
import csv
import pandas as pd
import ast

axis_accelerometer = 3
measures_per_axis = 10
name_csv = 'Patada.csv'
name_new_csv = 'kick.csv'

with open('csv/original/' + name_csv) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')

    df = []
    for row in csv_reader:
        column_count = 0
        for column in row:
            if column_count == 0:
                accelerometers = ast.literal_eval(column)
                accelerometers = np.array(list(map(int, accelerometers)))
                accelerometers = np.array_split(accelerometers,
                                                accelerometers.size / (axis_accelerometer * measures_per_axis))
            elif column_count == 1:
                if column == 'Dereita':
                    impact_label = 'right'
                elif column == 'Esquerda':
                    impact_label = 'left'
                else:
                    impact_label = 'frontal'
            else:
                power_measurement = column

            column_count += 1

        data = {}
        accelerometer_count = 0
        for accelerometer in accelerometers:
            accelerometer = np.array_split(accelerometer, axis_accelerometer)

            axis_count = 0
            for axis in accelerometer:
                if axis_count == 0:
                    axis_direction = 'X'
                elif axis_count == 1:
                    axis_direction = 'Y'
                else:
                    axis_direction = 'Z'

                measure_count = 0
                for measure in axis:
                    data['accelerometer' + str(accelerometer_count) + '_' + str(axis_direction)
                         + str(measure_count)] = measure

                    measure_count += 1

                axis_count += 1

            accelerometer_count += 1

        data['impact_label'] = impact_label
        data['power_measurement'] = power_measurement

        df.append(data)

df = pd.DataFrame(df)
df.to_csv('csv/generate/' + name_new_csv, encoding='utf-8', index=False)
