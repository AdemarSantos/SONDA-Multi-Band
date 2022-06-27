from Band_Selection import Band_Selection
from SSS import SSS
from Fiber import Fiber
from BoosterAmplifier import BoosterAmplifier
from InLineAmplifier import InLineAmplifier
from PreAmplifier import PreAmplifier

sss = SSS()
booster_amplifier = BoosterAmplifier()
inline_amplifier = InLineAmplifier()
pre_amplifier = PreAmplifier()
Band = Band_Selection()

"""
The Signal class represents a signal that propagates through the network.
"""

class Signal:

    def __init__(self, input_power = 0.001, input_OSNR = 1000):

        """
	:param input_power: input power of the network transmitters, in Watts.
	:param input_OSNR: input OSNR of the network.  
        """

        self.input_power = input_power
        self.input_OSNR = input_OSNR    

    def Summation(self, A, route, damp, fiber, freq):
        noise = []
        
        noise_figure = 5
        # Variable option below
        #noise_figure = Band.getNoiseFigureAmplifier_C(freq)
        
        for i in range(len(route)-1):
            dij = A[route[i]][route[i+1]]
            namp = inline_amplifier.NumberOfInlineAmplifiers(dij, damp)
            
            nb = booster_amplifier.Noise(sss.SSSLoss(), freq, noise_figure)
            ni = inline_amplifier.Noise(fiber.FiberLoss(dij), dij, damp, freq, noise_figure)
            np = pre_amplifier.Noise(fiber.FiberLoss(dij), namp, sss.SSSLoss(), freq, noise_figure)
                        
            noise.append(nb + (ni * (fiber.FiberLoss(dij)**(1/(1+namp)))) + (np/sss.SSSLoss()))
        summation = sum(noise)
        return summation
   
    def ModulationFormat(self, modulation_format):    
        return modulation_format    
    
    def InputPower(self):    
        return self.input_power

    def InputNoisePower(self):    
        input_noise_power = self.input_power/self.input_OSNR 
        return input_noise_power

    def OutputNoisePower(self, A, route, damp, fiber, freq):    
        output_noise_power = self.InputNoisePower() + self.Summation(A, route, damp, fiber, freq)
        return output_noise_power

    def OutputOSNR(self, A, route, damp, freq, fiber_type):
        fiber = Fiber(freq, fiber_type)       
        output_OSNR = self.input_power/self.OutputNoisePower(A, route, damp, fiber, freq)
        return output_OSNR