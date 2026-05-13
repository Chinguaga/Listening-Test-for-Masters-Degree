

#from imports import*
import numpy as np
import random
from config import *
import scipy 
# position of odd_sample
# the first sample in  the folder is the odd one

def gen_random_test():
    position_of_odd_sample = np.random.randint(0, 3, size= config['variations'] * config['trials']  )

    return position_of_odd_sample


def generate_unique_random_numbers(x):
    numbers = list(range(x + 1))  # Create a list from 0 to x
    random.shuffle(numbers)  # Shuffle the list
    return numbers  # Return the shuffled list



# ### Result Analysis
# class binominal_test:
#     def __init__(self, a, b):
#         # Local attributes a and b
#         self.a = a
#         self.b = b

#     def display_attributes(self):
#         # Method to display the values of attributes
#         print(f"a: {self.a}, b: {self.b}")
#     # Hypothesen test durch berechnender Teststatistik
#     n = config['trials'] # proably wrong -->Trials besteht aus Stimuli multipliziert mit der Anzahl von Personen 
#     # man kann den p wert (f_s) für indiviudelen und Gruppen berechnen
#     s = 9 # amount hits
#     alpha = 0.05/config['variations']    # Bonferroni correction# critical level # signifikanz nuveau
#     p = 1/3 # rate warscheinlichekit 3AFC = 0.333
#     p_pop = 0.9
#     #propability mass function # warscheinlichektisfunktion der binominal verteilung # Test statistik

#     #f_s = 0

#     print('H_0 = The phase distortions are not audible')

#     print('H_1 = The phase distortions are audible')

#     # Alpha error = The H_0 Hypothesis is incorretly neglected 
#     # The Phase differences are detected but dont acutally exist


#     def calc_alpha_error(s,n):
#         # propability that H_0 is rejected allthough there is no audible difference
#         print('the propability that ' + str(s) +' or more correct identifications occur, while H_0 is true ')
#         #propability that differences are audible when they are inaudible

#         # if this probability is small one could reject H_0 in favour of H_1

        
#         cum_sum = 0
        
#         for i in range(s,n+1):
#             s=i
#             #print(s)

#             binominal_koeffizient = scipy.special.factorial(n)/((scipy.special.factorial(s)* scipy.special.factorial(n-s)))
#             f_s_alpha = binominal_koeffizient * p**s * (1-p)**(n-s)
#             cum_sum += f_s_alpha

#         print('the Type 1/alpha error  is = ' + str(cum_sum)  )

#         if cum_sum<alpha==True:
#             print('H_0 gets rejected in favour of H_1')

#         return cum_sum 



#     def calc_beta_error(s,n,p_pop):
#         # propability that the H_= is not rejected allthough the differences are acutally not audible
#         # low power = high beta error propability

#         def power(beta):
#             return 1-beta

#         cum_sum = 0
        
#         for i in range(0,s):
#             s=i
#             #print(s)

#             binominal_koeffizient = scipy.special.factorial(n)/((scipy.special.factorial(s)* scipy.special.factorial(n-s)))
#             f_s_alpha = binominal_koeffizient * p_pop**s * (1-p_pop)**(n-s)
#             cum_sum += f_s_alpha

#         print('the Type 2/beta error  is = ' + str(cum_sum)  )

#         power = power(cum_sum)
#         print('the power is = ' + str(power))
#         #if cum_sum<alpha==True:
#         #    print('H_0 gets rejected in favour of H_1')

#         return cum_sum,power


class BinomialTest:
    def __init__(self, s, n, alpha, p, p_pop,num_variations):
        """
        Initializes the BinomialTest class.

        Parameters:
        s (int): Number of hits (correct identifications).
        n (int): Number of trials.
        alpha (float): Significance level (after Bonferroni correction).
        p (float): Probability of guessing correctly (e.g., 1/3 for 3AFC test).
        p_pop (float): Probability of true positive in population.
        """
        self.s = s
        self.n = n
        self.alpha = alpha/num_variations #Bonferroni correction
        self.p = p
        self.p_pop = p_pop

        print('H₀: The phase distortions are not audible.')
        print('H₁: The phase distortions are audible.')

    def calc_alpha_error(self):
        """
        Calculates the alpha error (Type I error).

        Returns:
        float: Probability that H₀ is rejected even though it is true.
        """
        print(f'Calculating Type I error (alpha) for {self.s} or more hits while H₀ is true...')
        cum_sum = 0
        for i in range(self.s, self.n + 1):
            binomial_coefficient = scipy.special.factorial(self.n) / (
                scipy.special.factorial(i) * scipy.special.factorial(self.n - i)
            )
            f_s_alpha = binomial_coefficient * self.p**i * (1 - self.p)**(self.n - i)
            cum_sum += f_s_alpha

        cum_sum = np.round(cum_sum,4)

        print(f'Type I error (alpha): {cum_sum:.5f}')
        if cum_sum < self.alpha:
            print('H₀ rejected in favor of H₁.')
        else:
            print('H₀ not rejected.')
        return cum_sum

    def calc_beta_error(self):
        """
        Calculates the beta error (Type II error) and statistical power.

        Returns:
        tuple: (beta error, power)
        """
        print(f'Calculating Type II error (beta) for {self.s} or fewer hits while H₁ is true...')
        cum_sum = 0
        for i in range(0, self.s):
            binomial_coefficient = scipy.special.factorial(self.n) / (
                scipy.special.factorial(i) * scipy.special.factorial(self.n - i)
            )
            f_s_beta = binomial_coefficient * self.p_pop**i * (1 - self.p_pop)**(self.n - i)
            cum_sum += f_s_beta

        beta_error = np.round(cum_sum,4)
        power = 1 - beta_error
        print(f'Type II error (beta): {beta_error:.5f}')
        print(f'Statistical power: {power:.5f}')
        return beta_error, power





## Varianz analyse

# Anova
# between subject <-> die Gruppen müssen komplettt unabhängig von einander sein, keine versuchsteilnehme dürfen beide conditions gmaht haben.
# 
# mixed measures Anova 
# 
# inbetween subject <-> Alle variations werden von allen versuchsteilnehmern bewertet.
#  