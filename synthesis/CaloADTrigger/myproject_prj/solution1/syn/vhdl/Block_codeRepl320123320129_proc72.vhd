-- ==============================================================
-- RTL generated by Vivado(TM) HLS - High-Level Synthesis from C, C++ and OpenCL
-- Version: 2020.1
-- Copyright (C) 1986-2020 Xilinx, Inc. All Rights Reserved.
-- 
-- ===========================================================

library IEEE;
use IEEE.std_logic_1164.all;
use IEEE.numeric_std.all;

entity Block_codeRepl320123320129_proc72 is
port (
    ap_clk : IN STD_LOGIC;
    ap_rst : IN STD_LOGIC;
    ap_start : IN STD_LOGIC;
    ap_done : OUT STD_LOGIC;
    ap_continue : IN STD_LOGIC;
    ap_idle : OUT STD_LOGIC;
    ap_ready : OUT STD_LOGIC;
    p_read : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read1 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read2 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read3 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read4 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read5 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read6 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read7 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read8 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read9 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read10 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read11 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read12 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read13 : IN STD_LOGIC_VECTOR (4 downto 0);
    p_read14 : IN STD_LOGIC_VECTOR (4 downto 0);
    link_out_0_V_i : IN STD_LOGIC_VECTOR (127 downto 0);
    link_out_0_V_o : OUT STD_LOGIC_VECTOR (127 downto 0);
    link_out_0_V_o_ap_vld : OUT STD_LOGIC );
end;


architecture behav of Block_codeRepl320123320129_proc72 is 
    constant ap_const_logic_1 : STD_LOGIC := '1';
    constant ap_const_logic_0 : STD_LOGIC := '0';
    constant ap_ST_fsm_state1 : STD_LOGIC_VECTOR (1 downto 0) := "01";
    constant ap_ST_fsm_state2 : STD_LOGIC_VECTOR (1 downto 0) := "10";
    constant ap_const_lv32_0 : STD_LOGIC_VECTOR (31 downto 0) := "00000000000000000000000000000000";
    constant ap_const_lv32_1 : STD_LOGIC_VECTOR (31 downto 0) := "00000000000000000000000000000001";
    constant ap_const_lv128_lc_1 : STD_LOGIC_VECTOR (127 downto 0) := "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000";
    constant ap_const_lv112_1 : STD_LOGIC_VECTOR (111 downto 0) := "0000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000001";
    constant ap_const_lv32_8 : STD_LOGIC_VECTOR (31 downto 0) := "00000000000000000000000000001000";
    constant ap_const_lv32_77 : STD_LOGIC_VECTOR (31 downto 0) := "00000000000000000000000001110111";
    constant ap_const_boolean_1 : BOOLEAN := true;

    signal ap_done_reg : STD_LOGIC := '0';
    signal ap_CS_fsm : STD_LOGIC_VECTOR (1 downto 0) := "01";
    attribute fsm_encoding : string;
    attribute fsm_encoding of ap_CS_fsm : signal is "none";
    signal ap_CS_fsm_state1 : STD_LOGIC;
    attribute fsm_encoding of ap_CS_fsm_state1 : signal is "none";
    signal ap_block_state1 : BOOLEAN;
    signal grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_start : STD_LOGIC;
    signal grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done : STD_LOGIC;
    signal grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_idle : STD_LOGIC;
    signal grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_ready : STD_LOGIC;
    signal grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_start_reg : STD_LOGIC := '0';
    signal ap_block_state1_ignore_call16 : BOOLEAN;
    signal ap_CS_fsm_state2 : STD_LOGIC;
    attribute fsm_encoding of ap_CS_fsm_state2 : signal is "none";
    signal p_Result_s_fu_191_p5 : STD_LOGIC_VECTOR (127 downto 0);
    signal link_out_0_V_o_preg : STD_LOGIC_VECTOR (127 downto 0) := "00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000";
    signal ap_NS_fsm : STD_LOGIC_VECTOR (1 downto 0);

    component dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s IS
    port (
        ap_clk : IN STD_LOGIC;
        ap_rst : IN STD_LOGIC;
        ap_start : IN STD_LOGIC;
        ap_done : OUT STD_LOGIC;
        ap_idle : OUT STD_LOGIC;
        ap_ready : OUT STD_LOGIC;
        data_0_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_1_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_2_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_3_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_4_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_5_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_6_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_7_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_8_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_9_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_10_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_11_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_12_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_13_V_read : IN STD_LOGIC_VECTOR (4 downto 0);
        data_14_V_read : IN STD_LOGIC_VECTOR (4 downto 0) );
    end component;



begin
    grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157 : component dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s
    port map (
        ap_clk => ap_clk,
        ap_rst => ap_rst,
        ap_start => grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_start,
        ap_done => grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done,
        ap_idle => grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_idle,
        ap_ready => grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_ready,
        data_0_V_read => p_read,
        data_1_V_read => p_read1,
        data_2_V_read => p_read2,
        data_3_V_read => p_read3,
        data_4_V_read => p_read4,
        data_5_V_read => p_read5,
        data_6_V_read => p_read6,
        data_7_V_read => p_read7,
        data_8_V_read => p_read8,
        data_9_V_read => p_read9,
        data_10_V_read => p_read10,
        data_11_V_read => p_read11,
        data_12_V_read => p_read12,
        data_13_V_read => p_read13,
        data_14_V_read => p_read14);





    ap_CS_fsm_assign_proc : process(ap_clk)
    begin
        if (ap_clk'event and ap_clk =  '1') then
            if (ap_rst = '1') then
                ap_CS_fsm <= ap_ST_fsm_state1;
            else
                ap_CS_fsm <= ap_NS_fsm;
            end if;
        end if;
    end process;


    ap_done_reg_assign_proc : process(ap_clk)
    begin
        if (ap_clk'event and ap_clk =  '1') then
            if (ap_rst = '1') then
                ap_done_reg <= ap_const_logic_0;
            else
                if ((ap_continue = ap_const_logic_1)) then 
                    ap_done_reg <= ap_const_logic_0;
                elsif (((grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done = ap_const_logic_1) and (ap_const_logic_1 = ap_CS_fsm_state2))) then 
                    ap_done_reg <= ap_const_logic_1;
                end if; 
            end if;
        end if;
    end process;


    grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_start_reg_assign_proc : process(ap_clk)
    begin
        if (ap_clk'event and ap_clk =  '1') then
            if (ap_rst = '1') then
                grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_start_reg <= ap_const_logic_0;
            else
                if ((not(((ap_start = ap_const_logic_0) or (ap_done_reg = ap_const_logic_1))) and (ap_const_logic_1 = ap_CS_fsm_state1))) then 
                    grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_start_reg <= ap_const_logic_1;
                elsif ((grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_ready = ap_const_logic_1)) then 
                    grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_start_reg <= ap_const_logic_0;
                end if; 
            end if;
        end if;
    end process;


    link_out_0_V_o_preg_assign_proc : process(ap_clk)
    begin
        if (ap_clk'event and ap_clk =  '1') then
            if (ap_rst = '1') then
                link_out_0_V_o_preg <= ap_const_lv128_lc_1;
            else
                if (((grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done = ap_const_logic_1) and (ap_const_logic_1 = ap_CS_fsm_state2))) then 
                    link_out_0_V_o_preg <= p_Result_s_fu_191_p5;
                end if; 
            end if;
        end if;
    end process;


    ap_NS_fsm_assign_proc : process (ap_start, ap_done_reg, ap_CS_fsm, ap_CS_fsm_state1, grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done, ap_CS_fsm_state2)
    begin
        case ap_CS_fsm is
            when ap_ST_fsm_state1 => 
                if ((not(((ap_start = ap_const_logic_0) or (ap_done_reg = ap_const_logic_1))) and (ap_const_logic_1 = ap_CS_fsm_state1))) then
                    ap_NS_fsm <= ap_ST_fsm_state2;
                else
                    ap_NS_fsm <= ap_ST_fsm_state1;
                end if;
            when ap_ST_fsm_state2 => 
                if (((grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done = ap_const_logic_1) and (ap_const_logic_1 = ap_CS_fsm_state2))) then
                    ap_NS_fsm <= ap_ST_fsm_state1;
                else
                    ap_NS_fsm <= ap_ST_fsm_state2;
                end if;
            when others =>  
                ap_NS_fsm <= "XX";
        end case;
    end process;
    ap_CS_fsm_state1 <= ap_CS_fsm(0);
    ap_CS_fsm_state2 <= ap_CS_fsm(1);

    ap_block_state1_assign_proc : process(ap_start, ap_done_reg)
    begin
                ap_block_state1 <= ((ap_start = ap_const_logic_0) or (ap_done_reg = ap_const_logic_1));
    end process;


    ap_block_state1_ignore_call16_assign_proc : process(ap_start, ap_done_reg)
    begin
                ap_block_state1_ignore_call16 <= ((ap_start = ap_const_logic_0) or (ap_done_reg = ap_const_logic_1));
    end process;


    ap_done_assign_proc : process(ap_done_reg, grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done, ap_CS_fsm_state2)
    begin
        if (((grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done = ap_const_logic_1) and (ap_const_logic_1 = ap_CS_fsm_state2))) then 
            ap_done <= ap_const_logic_1;
        else 
            ap_done <= ap_done_reg;
        end if; 
    end process;


    ap_idle_assign_proc : process(ap_start, ap_CS_fsm_state1)
    begin
        if (((ap_start = ap_const_logic_0) and (ap_const_logic_1 = ap_CS_fsm_state1))) then 
            ap_idle <= ap_const_logic_1;
        else 
            ap_idle <= ap_const_logic_0;
        end if; 
    end process;


    ap_ready_assign_proc : process(grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done, ap_CS_fsm_state2)
    begin
        if (((grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done = ap_const_logic_1) and (ap_const_logic_1 = ap_CS_fsm_state2))) then 
            ap_ready <= ap_const_logic_1;
        else 
            ap_ready <= ap_const_logic_0;
        end if; 
    end process;

    grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_start <= grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_start_reg;

    link_out_0_V_o_assign_proc : process(grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done, ap_CS_fsm_state2, p_Result_s_fu_191_p5, link_out_0_V_o_preg)
    begin
        if (((grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done = ap_const_logic_1) and (ap_const_logic_1 = ap_CS_fsm_state2))) then 
            link_out_0_V_o <= p_Result_s_fu_191_p5;
        else 
            link_out_0_V_o <= link_out_0_V_o_preg;
        end if; 
    end process;


    link_out_0_V_o_ap_vld_assign_proc : process(grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done, ap_CS_fsm_state2)
    begin
        if (((grp_dense_resource_ap_ufixed_ap_fixed_16_5_5_3_0_config6_s_fu_157_ap_done = ap_const_logic_1) and (ap_const_logic_1 = ap_CS_fsm_state2))) then 
            link_out_0_V_o_ap_vld <= ap_const_logic_1;
        else 
            link_out_0_V_o_ap_vld <= ap_const_logic_0;
        end if; 
    end process;

    p_Result_s_fu_191_p5 <= (link_out_0_V_i(127 downto 120) & ap_const_lv112_1 & link_out_0_V_i(7 downto 0));
end behav;
