import network


def connect(username, password):
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(username, password)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())


def disconnect():
    network.disconnect()
    print("disconnected from the network.")


def is_connected():
    sta_if = network.WLAN(network.STA_IF)
    return sta_if.isconnected()
