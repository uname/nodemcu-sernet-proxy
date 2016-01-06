-- SerialNet proxy v0.1
-- This is a data bridge for NodeMCU. Write these code to NodeMCU's init.lua and restart it.
-- NodeMCU will start in AP mode and proxy data between NET(TCP) and SERIAL(Rx/Tx)
-- If you want to quit from SerialNet proxy, just send '--quitproxy\r\n' from serial
-- Author: uname(github.com/uname)
---------------------------------------------
baud = 9600
serverPort = 8080
quitProxyCmd = "--quitproxy"
---------------------------------------------
client = nil
wifi.setmode(wifi.STATIONAP)
s = net.createServer(net.TCP, 2000)
s:listen(serverPort, function(c)
    client = c
    c:on("receive",
    function(c, data)
        uart.write(0, data)
    end )
    c:on("disconnection", function(c)
        client = nil
    end )
    end )
    
uart.setup(0, baud, 8, 0, 1, 0)
uart.on("data", function(data)
    if(data == quitProxyCmd) then
        print("proxy quit, bye")
        if(client ~= nil) then
            client:close()
        end
        s:close()
        uart.on("data")
    elseif(client ~= nil) then
        client:send(data)
    end
    end,
    0 )

print("\nScript by uname(github.com/uname)\nSerialNet proxy running on " .. wifi.ap.getip() .. ":"
 .. serverPort .. "\nType: " .. quitProxyCmd .. " in serial console to quit")
