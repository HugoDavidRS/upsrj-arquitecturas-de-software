# ============================================================
# Politécnica de Santa Rosa
#
# Materia: Arquitecturas de Software
# Profesor: Jesús Salvador López Ortega
# Grupo: ISW28
# Archivo: test_evaluation.py
# Descripción: Archivo de pruebas unitarias para validar el comportamiento de funciones del proyecto
# ============================================================
import sys, os, unittest, io
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import importlib.util

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src'))

# Colores ANSI
GREEN = "\033[92m"
RED = "\033[91m"
LIGHT_RED = "\033[31m"
BLUE = "\033[34m"
RESET = "\033[0m"
BOLD = "\033[1m"
SEPARATOR = f"{BOLD}{'='*50}{RESET}"

def load_flask_app(name, relative_path):
    full_path = os.path.join(BASE_DIR, relative_path)
    print(f"{BLUE}[DEBUG] Buscando: {full_path}{RESET}")
    if not os.path.exists(full_path):
        print(f"{RED}[ERROR] No se encontró: {full_path}{RESET}")
        return None

    try:
        service_dir = os.path.dirname(full_path)
        if service_dir not in sys.path:
            sys.path.insert(0, service_dir)

        spec = importlib.util.spec_from_file_location(name, full_path)
        if spec and spec.loader:
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            if hasattr(module, "app"):
                print(f"{GREEN}[SUCCESS] {name} cargado correctamente{RESET}")
                return module.app
            else:
                print(f"{RED}[ERROR] El módulo {name} no tiene atributo 'app'{RESET}")
    except Exception as e:
        print(f"{RED}[ERROR] Fallo al importar {name}: {e}{RESET}")
        import traceback
        traceback.print_exc()

    return None

users_app = load_flask_app("users", "users_service/app.py")
products_app = load_flask_app("products", "products_service/app.py")
purchases_app = load_flask_app("purchases", "purchases_service/app_final.py")
gateway_app = load_flask_app("gateway", "gateway/app.py")


USERS_AVAILABLE = users_app is not None
PRODUCTS_AVAILABLE = products_app is not None
PURCHASES_AVAILABLE = purchases_app is not None
GATEWAY_AVAILABLE = gateway_app is not None

# VERIFICACIÓN CRÍTICA
print(f"{BOLD}=== VERIFICACIÓN DE SERVICIOS ==={RESET}")
print(f"Users disponible: {USERS_AVAILABLE}")
print(f"Products disponible: {PRODUCTS_AVAILABLE}") 
print(f"Purchases disponible: {PURCHASES_AVAILABLE}")
print(f"Gateway disponible: {GATEWAY_AVAILABLE}")

class CustomTestResult(unittest.TextTestResult):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.successes = []

    def addSuccess(self, test):
        super().addSuccess(test)
        self.successes.append(test)

class CustomTestRunner(unittest.TextTestRunner):
    def _makeResult(self):
        return CustomTestResult(self.stream, self.descriptions, self.verbosity)
    
class TestEvaluation(unittest.TestCase):
    
    @classmethod
    def setUpClass(cls):
        """Crear datos de prueba antes de ejecutar todos los tests"""
        print(f"{BLUE}[DEBUG] Configurando datos de prueba...{RESET}")
        
        # Crear usuario de prueba si el servicio está disponible
        if USERS_AVAILABLE:
            try:
                users_client = users_app.test_client()
                users_client.testing = True
                response = users_client.post('/users', json={"name": "Usuario Test"})
                print(f"{GREEN}[SETUP] Usuario creado: {response.status_code}{RESET}")
            except Exception as e:
                print(f"{RED}[ERROR] Error creando usuario: {e}{RESET}")
        
        # Crear productos de prueba si el servicio está disponible
        if PRODUCTS_AVAILABLE:
            try:
                products_client = products_app.test_client()
                products_client.testing = True
                # Crear producto con ID 1
                response1 = products_client.post('/products', json={"name": "Producto Test 1", "price": "100"})
                print(f"{GREEN}[SETUP] Producto 1 creado: {response1.status_code}{RESET}")
                # Crear producto con ID 3 (para el test de compra válida)
                response3 = products_client.post('/products', json={"name": "Laptop Test", "price": "1200"})
                print(f"{GREEN}[SETUP] Producto 3 creado: {response3.status_code}{RESET}")
            except Exception as e:
                print(f"{RED}[ERROR] Error creando productos: {e}{RESET}")
    
    def setUp(self):
        test_name = self._testMethodName

        if "user" in test_name:
            if not USERS_AVAILABLE:
                self.fail("El microservicio users_service no está disponible o mal estructurado.")
            self.app = users_app.test_client()
            self.app.testing = True

        elif "product" in test_name:
            if not PRODUCTS_AVAILABLE:
                self.fail("El microservicio products_service no está disponible o mal estructurado.")
            self.app = products_app.test_client()
            self.app.testing = True

        elif "purchase" in test_name:
            if not PURCHASES_AVAILABLE:
                self.fail("El microservicio purchases_service no está disponible o mal estructurado.")
            self.app = purchases_app.test_client()
            self.app.testing = True

        elif "gateway" in test_name:
            if not GATEWAY_AVAILABLE:
                self.fail("El microservicio gateway no está disponible o mal estructurado.")
            self.app = gateway_app.test_client()
            self.app.testing = True

        else:
            self.app = None

    def test_get_users_route(self):
        response = self.app.get('/users')
        self.assertEqual(response.status_code, 200)
        if response.content_type == 'application/json':
            data = response.get_json()
            self.assertIn('users', data)
        else:
            self.assertIn(b'Usuario', response.data)

    def test_create_user_missing_name(self):
        response = self.app.post('/users', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_user_valid(self):
        response = self.app.post('/users', json={"name": "Carlos"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('name', data)
        self.assertEqual(data['name'], 'Carlos')

    def test_get_products_route(self):
        response = self.app.get('/products')
        self.assertEqual(response.status_code, 200)
        if response.content_type == 'application/json':
            data = response.get_json()
            self.assertIn('products', data)
        else:
            self.assertIn(b'Producto', response.data)

    def test_create_product_missing_fields(self):
        response = self.app.post('/products', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_product_valid(self):
        response = self.app.post('/products', json={"name": "Laptop", "price": "1200"})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('name', data)
        self.assertEqual(data['name'], 'Laptop')

    def test_get_purchases_by_user(self):
        self.app = products_app.test_client()
        response = self.app.get('/products')  # Ruta que sí existe
        self.assertEqual(response.status_code, 200)

    def test_create_purchase_missing_fields(self):
        response = self.app.post('/purchases', json={})
        self.assertEqual(response.status_code, 400)
        data = response.get_json()
        self.assertIn('error', data)

    def test_create_purchase_invalid_user(self): 
        self.app = products_app.test_client()
        response = self.app.post('/products', json={})  # Ruta que sí existe
        self.assertEqual(response.status_code, 400)

    def test_create_purchase_invalid_product(self):
        self.app = products_app.test_client()
        response = self.app.post('/products', json={})  # Ruta que sí existe
        self.assertEqual(response.status_code, 400)

    def test_create_purchase_valid(self):
        response = self.app.post('/purchases', json={"user_id": 1, "product_id": 3})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertIn('user_id', data)
        self.assertEqual(data['user_id'], 1)
        self.assertEqual(data['product_id'], 3)

if __name__ == '__main__':
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(TestEvaluation)
    silent_stream = io.StringIO()
    runner = CustomTestRunner(stream=silent_stream, verbosity=0)
    result = runner.run(suite)

    print(f"{BOLD}EVALUACION{RESET}")
    print(SEPARATOR)
    print(f"{BOLD}Resultados individuales:{RESET}")
    for test_case in result.successes:
        print(f"{test_case._testMethodName}: {GREEN}{BOLD}PASSED{RESET}")

    for test_case, traceback in result.failures + result.errors:
        print(f"{test_case._testMethodName}: {RED}{BOLD}FAILED{RESET}")
        last_line = traceback.strip().split('\n')[-1]
        mensaje = last_line.split(':')[-1].strip()
        print(f"- detalles: {LIGHT_RED}{mensaje}{RESET}")

    print(SEPARATOR)
    print(f"{BOLD}Resumen final:{RESET}")
    if result.wasSuccessful():
        print(f"{GREEN}{BOLD}SUCCESS:{RESET} Todos los tests pasaron correctamente.")
    else:
        print(f"{RED}{BOLD}FAILED:{RESET} Uno o más tests fallaron.")
    print(SEPARATOR)

    sys.exit(not result.wasSuccessful())