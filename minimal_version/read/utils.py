
def variableUnitsByChar(var_type):
    match var_type:
        case 'tensao':
            return {
                'name': "voltage",
                'unit': "V"}
        case 'corrente':
           return {
                'name': "current",
                'unit': "A"}
        case 'temperatura':
            return {
                'name': "temperature",
                'unit': "°C"}
        case 'vazao':
            return {
                'name': "flow_rate",
                'unit': "l/m"}
        case 'concentracao':
            return {
                'name': "hydrogen",
                'unit': "ppm"}
        case 'pulsos':
            return {
                'name': "pulse",
                'unit': "quantidade"}
        case _:
            print("Error: Tipo Invalido de Sensor")

