module Passthrough  #(parameter dataWidth=16,weightIntWidth=4) (
    input           clk,
    input   [2*dataWidth-1:0]   x,
    output  reg [dataWidth-1:0]  out
);
always @(posedge clk)
begin
    out <= x[dataWidth-1:0];
end

endmodule