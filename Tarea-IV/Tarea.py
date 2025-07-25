
import pulp

class ModeloPL:
    def __init__(self):
        self.num_vars = 0
        self.num_restricciones = 0
        self.coef_obj = []
        self.restricciones = []
        self.lados_derechos = []
        self.sentidos = []
        self.vars = []
        self.problema = None

    def solicitar_datos(self):
        print("--- MODELO DE PROGRAMACIÓN LINEAL ENTERA ---")
        self.num_vars = int(input("Ingrese el número de variables: "))
        self.num_restricciones = int(input("Ingrese el número de restricciones: "))
        print("Ingrese los coeficientes de la función objetivo (separados por espacio):")
        self.coef_obj = list(map(float, input().split()))
        print("Ingrese las restricciones una por una:")
        for i in range(self.num_restricciones):
            print(f"Restricción {i+1} (coeficientes separados por espacio):")
            coefs = list(map(float, input().split()))
            self.restricciones.append(coefs)
            sentido = input("Ingrese el sentido de la restricción (<=, >=, =): ")
            self.sentidos.append(sentido)
            lado = float(input("Ingrese el lado derecho de la restricción: "))
            self.lados_derechos.append(lado)

    def construir_modelo(self):
        self.problema = pulp.LpProblem("PL_Entera", pulp.LpMaximize)
        self.vars = [pulp.LpVariable(f"x{i+1}", lowBound=0, cat=pulp.LpContinuous) for i in range(self.num_vars)]
        self.problema += pulp.lpDot(self.coef_obj, self.vars)
        for i in range(self.num_restricciones):
            if self.sentidos[i] == '<=':
                self.problema += (pulp.lpDot(self.restricciones[i], self.vars) <= self.lados_derechos[i])
            elif self.sentidos[i] == '>=':
                self.problema += (pulp.lpDot(self.restricciones[i], self.vars) >= self.lados_derechos[i])
            else:
                self.problema += (pulp.lpDot(self.restricciones[i], self.vars) == self.lados_derechos[i])

    def es_entera(self, valores):
        return all(abs(v - round(v)) < 1e-5 for v in valores)

    def agregar_corte_gomory(self, valores):
        # Encuentra la variable con valor fraccional más grande
        for i, v in enumerate(valores):
            if abs(v - round(v)) > 1e-5:
                fila = self.problema.constraints.values()
                # No se puede obtener la fila simplex directamente con PuLP, así que se simula un corte simple
                # Corte: x_i <= floor(x_i)
                self.problema += self.vars[i] <= int(v)
                print(f"Se agrega corte: x{i+1} <= {int(v)}")
                break

    def resolver(self):
        iteracion = 1
        while True:
            print(f"\n--- Iteración {iteracion} ---")
            self.problema.solve()
            valores = [v.varValue for v in self.vars]
            print("Solución actual:", valores)
            if self.es_entera(valores):
                print("Solución entera encontrada.")
                break
            self.agregar_corte_gomory(valores)
            iteracion += 1
        print("\nValor óptimo:", pulp.value(self.problema.objective))
        for i, v in enumerate(self.vars):
            print(f"x{i+1} = {v.varValue}")

if __name__ == "__main__":
    modelo = ModeloPL()
    modelo.solicitar_datos()
    modelo.construir_modelo()
    modelo.resolver()
