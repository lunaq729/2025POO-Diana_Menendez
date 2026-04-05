-- TESTBENCH CON ASSERT PARA VERIFICACIÓN AUTOMÁTICA
-- Archivo: sumador_tb.vhd

library ieee;
use ieee.std_logic_1164.all;

entity sumador_tb is
end sumador_tb;

architecture test of sumador_tb is
    -- Declarar el componente que vamos a probar
    component sumador
        port(
            a, b, cin : in  std_logic;
            suma, cout: out std_logic
        );
    end component;
    
    -- Señales internas para conectar al componente
    signal s_a, s_b, s_cin : std_logic;
    signal s_suma, s_cout  : std_logic;
    
begin
    -- Instanciar el componente
    uut: sumador port map(
        a => s_a, 
        b => s_b, 
        cin => s_cin,
        suma => s_suma, 
        cout => s_cout
    );
    
    -- Proceso de estímulos con ASSERT
    process
    begin
        -- Caso 1: 0+0+0 = 0, acarreo=0
        s_a <= '0'; s_b <= '0'; s_cin <= '0'; wait for 20 ns;
        assert (s_suma = '0' and s_cout = '0') 
            report "ERROR: Caso 1 falló" severity error;
        
        -- Caso 2: 0+0+1 = 1, acarreo=0
        s_a <= '0'; s_b <= '0'; s_cin <= '1'; wait for 20 ns;
        assert (s_suma = '1' and s_cout = '0') 
            report "ERROR: Caso 2 falló" severity error;
        
        -- Caso 3: 0+1+0 = 1, acarreo=0
        s_a <= '0'; s_b <= '1'; s_cin <= '0'; wait for 20 ns;
        assert (s_suma = '1' and s_cout = '0') 
            report "ERROR: Caso 3 falló" severity error;
        
        -- Caso 4: 0+1+1 = 0, acarreo=1
        s_a <= '0'; s_b <= '1'; s_cin <= '1'; wait for 20 ns;
        assert (s_suma = '0' and s_cout = '1') 
            report "ERROR: Caso 4 falló" severity error;
        
        -- Caso 5: 1+0+0 = 1, acarreo=0
        s_a <= '1'; s_b <= '0'; s_cin <= '0'; wait for 20 ns;
        assert (s_suma = '1' and s_cout = '0') 
            report "ERROR: Caso 5 falló" severity error;
        
        -- Caso 6: 1+0+1 = 0, acarreo=1
        s_a <= '1'; s_b <= '0'; s_cin <= '1'; wait for 20 ns;
        assert (s_suma = '0' and s_cout = '1') 
            report "ERROR: Caso 6 falló" severity error;
        
        -- Caso 7: 1+1+0 = 0, acarreo=1
        s_a <= '1'; s_b <= '1'; s_cin <= '0'; wait for 20 ns;
        assert (s_suma = '0' and s_cout = '1') 
            report "ERROR: Caso 7 falló" severity error;
        
        -- Caso 8: 1+1+1 = 1, acarreo=1
        s_a <= '1'; s_b <= '1'; s_cin <= '1'; wait for 20 ns;
        assert (s_suma = '1' and s_cout = '1') 
            report "ERROR: Caso 8 falló" severity error;
        
        -- Mensaje final de éxito
        report "✔ TODOS LOS CASOS PASARON LA VERIFICACIÓN" severity note;
        
        wait; -- Fin de la simulación
    end process;
end test;