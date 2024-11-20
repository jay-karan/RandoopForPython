import random
import string

def generate_random_primitive(param_type, storage=None):
    if param_type == int:
        return random.randint(-100, 100)
    elif param_type == float:
        return random.uniform(-100, 100)
    elif param_type == str:
        return ''.join(random.choices(string.ascii_letters, k=5))
    elif param_type == bool:
        return random.choice([True, False])
    elif param_type == list:
        return [generate_random_primitive(random.choice([int, float, str])) for _ in range(random.randint(1, 5))]
    elif param_type == tuple:
        return tuple(generate_random_primitive(random.choice([int, float, str])) for _ in range(random.randint(1, 5)))
    elif param_type == dict:
        return {
            generate_random_primitive(str): generate_random_primitive(random.choice([int, float, str]))
            for _ in range(random.randint(1, 5))
        }
    elif param_type == set:
        return {generate_random_primitive(random.choice([int, str])) for _ in range(random.randint(1, 5))}
    elif param_type == complex:
        return complex(random.randint(-100, 100), random.randint(-100, 100))
    elif isinstance(param_type, type):
        if storage and param_type.__name__ in storage:
            return random.choice(storage[param_type.__name__])
        else:
            try:
                return param_type()
            except Exception as e:
                print(f"Error: Could not instantiate {param_type.__name__}: {e}")
                return None
    else:
        print(f"Warning: Unknown type {param_type}. Returning None.")
        return None
