from enum import Enum


class MCP23017(Enum):
    # MCP23017 base address
    ADDRESS = 0x20

    # registers for A side
    IODIRA = 0x00
    IPOLA = 0x02
    GPINTENA = 0x04
    DEFVALA = 0x06
    INTCONA = 0x08
    IOCONA = 0x0A
    GPPUA = 0x0C
    INTFA = 0x0E
    INTCAPA = 0x10
    GPIOA = 0x12
    OLATA = 0x14

    # registers for B side
    IODIRB = 0x01
    IPOLB = 0x03
    GPINTENB = 0x05
    DEFVALB = 0x07
    INTCONB = 0x09
    IOCONB = 0x0B
    GPPUB = 0x0D
    INTFB = 0x0F
    INTCAPB = 0x11
    GPIOB = 0x13
    OLATB = 0x15
