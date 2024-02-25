module ReLU  #(parameter dataWidth=16,weightIntWidth=4) (
    input           clk,
    input   [2*dataWidth-1:0]   x,
    output  reg [dataWidth-1:0]  out
);


always @(posedge clk)
begin
    if($signed(x) >= 0)
    begin
        if(|x[2*dataWidth-1:dataWidth]) //over flow to sign bit of integer part
            out <= {1'b0,{(dataWidth-1){1'b1}}}; //positive saturate
        else
            out <= x[dataWidth-1:0];
    end
    else 
        out <= 0;      
end

endmodule