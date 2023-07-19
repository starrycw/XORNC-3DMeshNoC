`timescale 1ns / 1ps
//////////////////////////////////////////////////////////////////////////////////
// Company: 
// Engineer: 
// 
// Create Date: 2023/07/19 13:48:01
// Design Name: 
// Module Name: arbiterNCModule_EncodingRules
// Project Name: 
// Target Devices: 
// Tool Versions: 
// Description: 
// 
// Dependencies: 
// 
// Revision:
// Revision 0.01 - File Created
// Additional Comments:
// 
//////////////////////////////////////////////////////////////////////////////////
`include "design_params.vh "

module arbiterNCModule_EncodingRules_WE(
    input wire [6 : 0] W_AddrCompare, E_AddrCompare,
    output reg if_sat,
    output reg [6 : 0] Forward_directions
    );
    
    wire W_XDestiEqual = ( ~W_AddrCompare[`IDX_W] ) & ( ~W_AddrCompare[`IDX_E] );
    wire W_YDestiEqual = ( ~W_AddrCompare[`IDX_S] ) & ( ~W_AddrCompare[`IDX_N] );
    wire W_ZDestiEqual = ( ~W_AddrCompare[`IDX_D] ) & ( ~W_AddrCompare[`IDX_U] );
    
    wire E_XDestiEqual = ( ~E_AddrCompare[`IDX_W] ) & ( ~E_AddrCompare[`IDX_E] );
    wire E_YDestiEqual = ( ~E_AddrCompare[`IDX_S] ) & ( ~E_AddrCompare[`IDX_N] );
    wire E_ZDestiEqual = ( ~E_AddrCompare[`IDX_D] ) & ( ~E_AddrCompare[`IDX_U] );
    
    // Condition A: Two destinations locate at the same XY plane as the local router. 
    wire sat_A_condition1, sat_A_condition2, sat_A;
//    assign sat_A_condition1 = ( (~W_AddrCompare[`IDX_W]) & (~E_AddrCompare[`IDX_E]) ) | ( (~W_AddrCompare[`IDX_E]) & (~E_AddrCompare[`IDX_W]) );
    assign sat_A_condition1 = 1'b1;
    assign sat_A_condition2 = ( W_AddrCompare[`IDX_S] & E_AddrCompare[`IDX_S] ) | ( W_AddrCompare[`IDX_N] & E_AddrCompare[`IDX_N] );
    assign sat_A = sat_A_condition1 & sat_A_condition2 & W_ZDestiEqual & E_ZDestiEqual;
    
    // Condition B: Two destinations locate at the same XZ plane as the local router. 
    wire sat_B_condition1, sat_B_condition2, sat_B;
//    assign sat_B_condition1 = ( (~W_AddrCompare[`IDX_W]) & (~E_AddrCompare[`IDX_E]) ) | ( (~W_AddrCompare[`IDX_E]) & (~E_AddrCompare[`IDX_W]) );
    assign sat_B_condition1 = 1'b1;
    assign sat_B_condition2 = ( W_AddrCompare[`IDX_D] & E_AddrCompare[`IDX_D] ) | ( W_AddrCompare[`IDX_U] & E_AddrCompare[`IDX_U] );
    assign sat_B = sat_B_condition1 & sat_B_condition2  & W_YDestiEqual & E_YDestiEqual;
    
    // Condition C: Take the XZ plane as the reference plane of sources. Not all the destinations locate at the same plane as the local router.
    wire all_same_plane = (W_XDestiEqual & E_XDestiEqual) | (W_YDestiEqual & E_YDestiEqual) | (W_ZDestiEqual & E_ZDestiEqual);
    wire sat_C;
    assign sat_C = (~all_same_plane) & ( ((~W_AddrCompare[`IDX_S]) & (~E_AddrCompare[`IDX_S])) | ((~W_AddrCompare[`IDX_N]) & (~E_AddrCompare[`IDX_N])) );
    
    // Condition D: Take the XY plane as the reference plane of sources. Not all the destinations locate at the same plane as the local router.
    wire sat_D;
    assign sat_D = (~all_same_plane) & ( ((~W_AddrCompare[`IDX_D]) & (~E_AddrCompare[`IDX_D])) | ((~W_AddrCompare[`IDX_U]) & (~E_AddrCompare[`IDX_U])) );
    
    // Rules
    reg [6 : 0] Forward_direction_C01W, Forward_direction_C01E, Forward_direction_D01W, Forward_direction_D01E; //用于处理condition C & D中存在同平面目标地址时的情况。
    
    
    always @(*) begin
        
        if (W_AddrCompare[`IDX_IP] | E_AddrCompare[`IDX_IP]) begin
            if_sat = 1'b0;
            Forward_directions = 7'b00_00_00_0;
        end
        
        else if (sat_A) begin
            if_sat = 1'b1;
            Forward_directions = (7'b00_11_00_0) & W_AddrCompare;
        end
        
        else if (sat_B) begin
            if_sat = 1'b1;
            Forward_directions = (7'b11_00_00_0) & W_AddrCompare;
        end
        
        else if (sat_C) begin
            if_sat = 1'b1;
            Forward_direction_C01W = (W_YDestiEqual) ? ( (W_ZDestiEqual) ? ( (7'b00_00_11_0) & (W_AddrCompare) ) : ( (7'b11_00_00_0) & (W_AddrCompare) ) ) : ( 7'b00_00_00_0 );
            Forward_direction_C01E = (E_YDestiEqual) ? ( (E_ZDestiEqual) ? ( (7'b00_00_11_0) & (E_AddrCompare) ) : ( (7'b11_00_00_0) & (E_AddrCompare) ) ) : ( 7'b00_00_00_0 );
            Forward_directions = ( (7'b00_11_00_0) & W_AddrCompare ) | ( (7'b00_11_00_0) & E_AddrCompare ) | Forward_direction_C01W | Forward_direction_C01E;
        end
        
        else if (sat_D) begin
            if_sat = 1'b1;
            Forward_direction_D01W = (W_ZDestiEqual) ? ( (W_YDestiEqual) ? ( (7'b00_00_11_0) & (W_AddrCompare) ) : ( (7'b00_11_00_0) & (W_AddrCompare) ) ) : ( 7'b00_00_00_0 );
            Forward_direction_D01E = (E_ZDestiEqual) ? ( (E_YDestiEqual) ? ( (7'b00_00_11_0) & (E_AddrCompare) ) : ( (7'b00_11_00_0) & (E_AddrCompare) ) ) : ( 7'b00_00_00_0 );
            Forward_directions = ( (7'b11_00_00_0) & W_AddrCompare ) | ( (7'b11_00_00_0) & E_AddrCompare ) | Forward_direction_D01W | Forward_direction_D01E;
        end
        
        else begin
            if_sat = 1'b0;
            Forward_directions = 7'b00_00_00_0;
        end
        
    end
    
endmodule

////////////////////////////////////////////////////////////////////////////////////////////////////////////
module arbiterNCModule_EncodingRules_SN(
    input wire [6 : 0] S_AddrCompare, N_AddrCompare,
    output reg if_sat,
    output reg [6 : 0] Forward_directions
    );
    
    wire S_XDestiEqual = ( ~S_AddrCompare[`IDX_W] ) & ( ~S_AddrCompare[`IDX_E] );
    wire S_YDestiEqual = ( ~S_AddrCompare[`IDX_S] ) & ( ~S_AddrCompare[`IDX_N] );
    wire S_ZDestiEqual = ( ~S_AddrCompare[`IDX_D] ) & ( ~S_AddrCompare[`IDX_U] );
    
    wire N_XDestiEqual = ( ~N_AddrCompare[`IDX_W] ) & ( ~N_AddrCompare[`IDX_E] );
    wire N_YDestiEqual = ( ~N_AddrCompare[`IDX_S] ) & ( ~N_AddrCompare[`IDX_N] );
    wire N_ZDestiEqual = ( ~N_AddrCompare[`IDX_D] ) & ( ~N_AddrCompare[`IDX_U] );
    
    // Condition A: Two destinations locate at the same YZ plane as the local router. 
    wire sat_A_condition1, sat_A_condition2, sat_A;
//    assign sat_A_condition1 = ( (~S_AddrCompare[`IDX_S]) & (~N_AddrCompare[`IDX_N]) ) | ( (~S_AddrCompare[`IDX_N]) & (~N_AddrCompare[`IDX_S]) );
    assign sat_A_condition1 = 1'b1;
    assign sat_A_condition2 = ( S_AddrCompare[`IDX_D] & N_AddrCompare[`IDX_D] ) | ( S_AddrCompare[`IDX_U] & N_AddrCompare[`IDX_U] );
    assign sat_A = sat_A_condition1 & sat_A_condition2 & S_XDestiEqual & N_XDestiEqual;
    
    // Condition B : Two destinations locate at the same XY plane as the local router. (X)
    
    
    // Condition C: Take the XZ plane as the reference plane of sources. Not all the destinations locate at the same plane as the local router. (X)
    
    
    // Condition D: Take the XY plane as the reference plane of sources. Not all the destinations locate at the same plane as the local router. (X)
    
    
    // Rules
   
    always @(*) begin
        
        if (S_AddrCompare[`IDX_IP] | N_AddrCompare[`IDX_IP]) begin
            if_sat = 1'b0;
            Forward_directions = 7'b00_00_00_0;
        end
        
        else if (sat_A) begin
            if_sat = 1'b1;
            Forward_directions = (7'b11_00_00_0) & S_AddrCompare;
        end
         
        else begin
            if_sat = 1'b0;
            Forward_directions = 7'b00_00_00_0;
        end
        
    end
    
endmodule
