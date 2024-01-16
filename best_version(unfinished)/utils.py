def variableUnitsByChar(var_type):
    match var_type:
        case 'v':
            return {
                'name': "voltage",
                'unit': "V"}
        case 'c':
           return {
                'name': "current",
                'unit': "A"}
        case 't':
            return {
                'name': "temperature",
                'unit': "°C"}
        case 'f':
            return {
                'name': "flow_rate",
                'unit': "l/m"}
        case 'h':
            return {
                'name': "hydrogen",
                'unit': "ppm"}
        case _:
            print("Error: Tipo Invalido de Sensor")

