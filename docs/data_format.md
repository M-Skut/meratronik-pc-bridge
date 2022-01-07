# Data Frame format
The code in this repository is communicating via UART to Python application.
To transfer data in lore or less reliable way a simple protocol was developed.
It's far from ideal (Still better than sending JSON)but the measurement 
can be read without any decoding using any serial terminal program.

## Data frame

```c
char dataPacket[] = {'$', 'R', 'T', 'S', 1, 1, 1, 1, 1, '\r', '\n'};
```

The first char `$` is used to synchronize the packets. The second char is used
to determine measurement range or report any errors.

| Char | Meaning |
| ---- | ------- |
| `A` | 100 mV measurement range |
| 'B' | 1 V  measurement range |
| 'C' | 10V  measurement range |
| 'D' | 100V  measurement range |
| 'E' | 1000V  measurement range |
| `O` | Measurement over-range |
| 'G' | Digit 0 (Least significant) does not have correct BCD code |
| 'H' | Digit 1 does not have correct BCD code |
| 'I' | Digit 2 does not have correct BCD code |
| 'J' | Digit 3 does not have correct BCD code |
| 'K' | Measurement range couldn't be decoded |
| 'L' | Measurement type couldn't be decoded |
| 'M' | Measurement sign couldn't be decoded |

All of those error should mean that come connections on PCB, cable or in the
voltage meter itself is defective and further investigation will be needed.

The third char communicates type of measurement - AC or DC.
| Char | Meaning |
| ---- | ------- |
| 'A' | AC measurement |
| 'D' | DC measurement |

The forth char communicates sign of measurement - plus or minus
| Char | Meaning |
| ---- | ------- |
| 'P' | Positive voltage value |
| 'M' | Negative voltage value |

The next 5 chars is raw number from device digits.

The last two chars are used to format the frame to be readable in any terminal.