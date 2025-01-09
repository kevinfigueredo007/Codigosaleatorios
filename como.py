import struct

def unpack_comp1(data):
    """Descompactar COMP-1 (ponto flutuante simples, 4 bytes)."""
    return struct.unpack('>f', data)[0]  # '>f' para float em big-endian (COBOL usa big-endian por padrão).

def unpack_comp2(data):
    """Descompactar COMP-2 (ponto flutuante duplo, 8 bytes)."""
    return struct.unpack('>d', data)[0]  # '>d' para double em big-endian.

def unpack_comp3(data, num_digits):
    """
    Descompactar COMP-3 (packed decimal).
    - data: bytes do número COMP-3.
    - num_digits: número total de dígitos esperados.
    """
    result = ''
    for byte in data[:-1]:  # Até o penúltimo byte
        result += f'{(byte >> 4) & 0xF}{byte & 0xF}'  # Extrai os dois dígitos.

    # Último byte contém o último dígito e o sinal.
    last_byte = data[-1]
    result += f'{(last_byte >> 4) & 0xF}'  # Extrai o último dígito.
    sign = last_byte & 0xF  # Extrai o sinal.

    if sign == 0xD:  # Negativo
        return f'-{result}'
    elif sign == 0xC:  # Positivo
        return result
    else:
        raise ValueError("Formato COMP-3 inválido ou não reconhecido.")

# Exemplo de uso
if __name__ == "__main__":
    # COMP-1: Número armazenado como 4 bytes (float simples)
    comp1_data = b'\x41\x20\x00\x00'  # Representa o número 10.0
    print("COMP-1:", unpack_comp1(comp1_data))

    # COMP-2: Número armazenado como 8 bytes (float duplo)
    comp2_data = b'\x40\x24\x00\x00\x00\x00\x00\x00'  # Representa o número 10.0
    print("COMP-2:", unpack_comp2(comp2_data))

    # COMP-3: Número decimal compactado
    comp3_data = b'\x12\x34\x5C'  # Representa o número +12345
    print("COMP-3:", unpack_comp3(comp3_data, num_digits=5))