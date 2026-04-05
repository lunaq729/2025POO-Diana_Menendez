-- SUMADOR COMPLETO DE 1 BIT
-- Archivo: sumador.vhd

library ieee;
use ieee.std_logic_1164.all;

entity sumador is
    port(
        a, b, cin : in  std_logic;   -- Cin = acarreo de entrada
        suma      : out std_logic;   -- Resultado de la suma
        cout      : out std_logic    -- Acarreo de salida
    );
end sumador;

architecture flujo_datos of sumador is
begin
    -- Ecuaciones correctas del sumador completo
    suma <= a xor b xor cin;
    cout <= (a and b) or (a and cin) or (b and cin);
end flujo_datos;