[hill_huxley]: ./results/equations/hill_huxley_model.png
[activation_dynamics]: ./results/equations/activation_dynamics.png
[force_dynamics]: ./results/equations/force_dynamics.png
[fatigue_dynamics]: ./results/equations/fatigue_dynamics.png
[strength_index]: ./results/equations/strength_index.png
[state_variables]: ./results/equations/state_variables.png
[face_validity]: ./results/face_validity.png
[comparison]: ./results/comparison_validity.png
[comparison_table]: ./results/comparison_validity_table.png
[simulation_plots]: ./results/sample_simulations.png
[rankings]: ./results/final_rankings.png
[50hz_plots]: ./results/50hz_plots.png

#Optimization of Electrical Stimulation Parameters for the Quadriceps Femoris Muscle

##Knee Osteoarthritis & NMES
Osteoarthritis (OA) is the most common form of arthritis and affects approximately 10% of the population over the age 
of 55. Individuals suffering from OA experience pain in and around their knee, with this pain worsening under 
weight-bearing activities. OA is also a major cause of early retirement, as it leads to significant pain and 
disability in 1/3 of those affected, making the socioeconomic burden associated with OA large. As there is no cure 
for knee OA, barring total replacement, treatment primarily consists of symptom management, with neuromuscular 
electrical stimulation (NMES) being one of the most effective methods. NMES relieves pain by applying a series of 
intermittent electrical stimuli, via electrodes placed on the skin, to superficial muscles to trigger contractions. 
For knee OA, NMES is typically used to strengthen the quadriceps femoris through electrodes on the anterior thigh. 
This stimulation increases muscle length and thickness, leading to better force distribution and stability at the knee 
joint.

Despite the wide availability of NMES units, there are currently no standard treatment parameters for NMES devices. 
Due to the crucial importance NMES parameters in treatment and lack of consensus among previous studies, the goal of 
this project is to determine the optimal NMES frequency and stimulation pulse type for knee OA treatment. This will 
consist of determining which parameters produce the most sustained force with minimal fatigue over time to optimize 
quadricep strength retention. To achieve this goal, a musculoskeletal model of the isometric contraction in the 
rectus femoris quadricep muscle was created in Python.

##Model Dynamics & Equations
Modified Hill-Huxley Model of Quadriceps Femoris:

![hill_huxley]

Activation Dynamics:

![activation_dynamics]

Force Dynamics:

![force_dynamics]

Fatigue Dynamics:

![fatigue_dynamics]

State Variables:

![state_variables]

To compare the results and avoid trivial solutions (higher frequency = more force = more fatigue),
the following strength index equation was developed. From literature, it was found that the level of fatigue during a 
typical stimulation session, as well as the amount of work done by the muscle, were the two most common
indicators for patient progression. As such, the index was set equal to the response’s
force-time integral scaled by the amount of incurred fatigue. The scale factor due to fatigue was
characterized by the normalized root-mean-square error (NRMSE) of the force response, where
the “observed” value in each calculation, Fmax, was a constant equal to the peak force in the simulated
simulated response. This scale factor was required, as the experiments utilized three different stimulation types which 
were seen to provoke different magnitudes in peak force response. Relying solely on the force-time integral would be 
insufficient, as a DFT protocol would evidently cause larger forces, especially at the beginning, than a CFT would, 
thereby skewing the integral value during comparison. To validate the applicability of this equation for the project, 
assumptions and restrictions were defined. Firstly, it was assumed that peak force occurred during the start of the 
contraction protocol within the first series of pulses sent. This was defined due to similar behavior seen in force 
response data from literature and was important in enabling the NRMSE, as calculated in the project, to truly 
characterize induced fatigue. The second assumption was that the peak force for a response would be non-zero, as 
restricted by the NRMSE term. Finally, the third assumption was that the index was valid for a fixed time interval, 
since the lengths of NMES sessions are fixed. For the project’s use, index would be a single subject measure that 
enables inter-session comparison to track a subject’s muscle force physiology over many NMES sessions.

![strength_index]

##Verification & Validation
###Face Validity
Model State Trajectories to 1 Hz CFT & 50 Hz CFT:

![face_validity]

###Comparison to Experimental Data
Predicted vs. Experimental Force Response of Model to A DFT155 Fatiguing Protocol:

![comparison]

![comparison_table]


##Simulations & Results

Sample Force vs. Time Simulation Plots:

![simulation_plots]

Final Strength Index Rankings:

![rankings]

Sample Stimulation & Force Response of DFT 50 Hz:

![50hz_plots]

##Future Improvements
- Collect experimental data to provide better overview of entire NMES process
- Redesign model to account for additional NMES stimulation parameters, such as
pulse width and amplitude
- Utilize more than one set of parameters to account for physiological variance
- Consult with professional in the field to formulate a more accurate, clinically approved
comparison strength index
- Experiment with different combination of fatiguing protocols
- Validate model on stimulation types it was not parametrized with
