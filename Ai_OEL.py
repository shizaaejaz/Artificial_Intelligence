import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def initialize_population(job_schedule_pool_size, num_tasks, num_machines):
    """Create an initial population of task-to-machine assignments."""
    population = []
    for _ in range(job_schedule_pool_size):
        individual = [random.randint(0, num_machines - 1) for _ in range(num_tasks)]
        population.append(individual)
    return population

def fitness_function(individual, task_durations, num_machines):
    """Calculate the fitness of a schedule based on makespan (minimizing max completion time)."""
    machine_times = [0] * num_machines
    for task, machine in enumerate(individual):
        machine_times[machine] += task_durations[task]
    return -max(machine_times)  # Negate because we minimize makespan

def selection(population, fitness_scores):
    """Select two parents based on their fitness scores using roulette wheel selection."""
    total_fitness = sum(fitness_scores)
    probabilities = [fitness / total_fitness for fitness in fitness_scores]
    return random.choices(population, probabilities, k=2)

def crossover(parent1, parent2):
    """Perform single-point crossover to produce two offspring."""
    point = random.randint(1, len(parent1) - 1)
    offspring1 = parent1[:point] + parent2[point:]
    offspring2 = parent2[:point] + parent1[point:]
    return offspring1, offspring2

def mutate(individual, adjustment_probability, num_machines):
    """Mutate an individual by randomly reassigning tasks to machines."""
    for i in range(len(individual)):
        if random.random() < adjustment_probability:
            individual[i] = random.randint(0, num_machines - 1)
    return individual

def genetic_algorithm_job_scheduling(job_schedule_pool_size, task_durations, num_machines, iteration_limit, adjustment_probability):
    """Run a genetic algorithm to optimize job scheduling."""
    num_tasks = len(task_durations)
    population = initialize_population(job_schedule_pool_size, num_tasks, num_machines)

    results = []
    for generation in range(iteration_limit):
        fitness_scores = [
            fitness_function(individual, task_durations, num_machines) for individual in population
        ]
        best_fitness = max(fitness_scores)
        results.append(f"Generation {generation + 1}: Best Makespan = {-best_fitness}")

        if -best_fitness <= min(task_durations):  # Ideal case: smallest possible makespan
            results.append("\nOptimal scheduling found with minimum makespan!")
            break

        next_generation = []
        while len(next_generation) < job_schedule_pool_size:
            parent1, parent2 = selection(population, fitness_scores)
            offspring1, offspring2 = crossover(parent1, parent2)
            next_generation.append(mutate(offspring1, adjustment_probability, num_machines))
            next_generation.append(mutate(offspring2, adjustment_probability, num_machines))

        population = next_generation[:job_schedule_pool_size]

    best_individual = max(population, key=lambda ind: fitness_function(ind, task_durations, num_machines))
    best_makespan = -fitness_function(best_individual, task_durations, num_machines)

    results.append("\nOptimal Schedule Found:")
    for task, machine in enumerate(best_individual):
        results.append(f"Task {task + 1} -> Machine {machine + 1}")
    results.append(f"\nMinimum Makespan: {best_makespan}")

    return results, best_individual, best_makespan

def run_genetic_algorithm():
    try:
        num_tasks = int(task_count_entry.get())
        num_machines = int(machine_count_entry.get())
        task_durations = list(map(int, task_durations_entry.get().split()))
        job_schedule_pool_size = int(population_size_entry.get())
        iteration_limit = int(generation_count_entry.get())
        adjustment_probability = float(mutation_rate_entry.get())

        if len(task_durations) != num_tasks:
            raise ValueError("Number of task durations does not match the number of tasks.")

        results, _, _ = genetic_algorithm_job_scheduling(
            job_schedule_pool_size, task_durations, num_machines, iteration_limit, adjustment_probability
        )

        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, "\n".join(results))

    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

# Create the GUI
root = tk.Tk()
root.title("Job Scheduling Optimizer")
root.configure(bg="#f3e5f5")  # Light purple background

# Style Configuration
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 10), background="#f3e5f5")
style.configure("TButton", font=("Helvetica", 10), background="#d1c4e9")

# Input labels and fields
ttk.Label(root, text="Number of Tasks:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
task_count_entry = ttk.Entry(root)
task_count_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Number of Machines:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
machine_count_entry = ttk.Entry(root)
machine_count_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="Task Durations (space-separated):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
task_durations_entry = ttk.Entry(root)
task_durations_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(root, text="Population Size:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
population_size_entry = ttk.Entry(root)
population_size_entry.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(root, text="Number of Generations:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
generation_count_entry = ttk.Entry(root)
generation_count_entry.grid(row=4, column=1, padx=10, pady=5)

ttk.Label(root, text="Mutation Rate (e.g., 0.01 for 1%):").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
mutation_rate_entry = ttk.Entry(root)
mutation_rate_entry.grid(row=5, column=1, padx=10, pady=5)

# Run button
run_button = ttk.Button(root, text="Run Optimization", command=run_genetic_algorithm)
run_button.grid(row=6, column=0, columnspan=2, pady=10)

# Results display
ttk.Label(root, text="Results:").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
results_text = tk.Text(root, height=15, width=50, bg="#ede7f6", font=("Helvetica", 10))  # Purple tint background
results_text.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Heading styling
header_label = tk.Label(root, text="Job Scheduling Optimizer", font=("Helvetica", 16, "bold", "underline"), bg="#f3e5f5")
header_label.grid(row=9, column=0, columnspan=2, pady=10)

# Start the GUI loop
root.mainloop()
import random
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk

def initialize_population(job_schedule_pool_size, num_tasks, num_machines):
    """Create an initial population of task-to-machine assignments."""
    population = []
    for _ in range(job_schedule_pool_size):
        individual = [random.randint(0, num_machines - 1) for _ in range(num_tasks)]
        population.append(individual)
    return population

def fitness_function(individual, task_durations, num_machines):
    """Calculate the fitness of a schedule based on makespan (minimizing max completion time)."""
    machine_times = [0] * num_machines
    for task, machine in enumerate(individual):
        machine_times[machine] += task_durations[task]
    return -max(machine_times)  # Negate because we minimize makespan

def selection(population, fitness_scores):
    """Select two parents based on their fitness scores using roulette wheel selection."""
    total_fitness = sum(fitness_scores)
    probabilities = [fitness / total_fitness for fitness in fitness_scores]
    return random.choices(population, probabilities, k=2)

def crossover(parent1, parent2):
    """Perform single-point crossover to produce two offspring."""
    point = random.randint(1, len(parent1) - 1)
    offspring1 = parent1[:point] + parent2[point:]
    offspring2 = parent2[:point] + parent1[point:]
    return offspring1, offspring2

def mutate(individual, adjustment_probability, num_machines):
    """Mutate an individual by randomly reassigning tasks to machines."""
    for i in range(len(individual)):
        if random.random() < adjustment_probability:
            individual[i] = random.randint(0, num_machines - 1)
    return individual

def genetic_algorithm_job_scheduling(job_schedule_pool_size, task_durations, num_machines, iteration_limit, adjustment_probability):
    """Run a genetic algorithm to optimize job scheduling."""
    num_tasks = len(task_durations)
    population = initialize_population(job_schedule_pool_size, num_tasks, num_machines)

    results = []
    for generation in range(iteration_limit):
        fitness_scores = [
            fitness_function(individual, task_durations, num_machines) for individual in population
        ]
        best_fitness = max(fitness_scores)
        results.append(f"Generation {generation + 1}: Best Makespan = {-best_fitness}")

        if -best_fitness <= min(task_durations):  # Ideal case: smallest possible makespan
            results.append("\nOptimal scheduling found with minimum makespan!")
            break

        next_generation = []
        while len(next_generation) < job_schedule_pool_size:
            parent1, parent2 = selection(population, fitness_scores)
            offspring1, offspring2 = crossover(parent1, parent2)
            next_generation.append(mutate(offspring1, adjustment_probability, num_machines))
            next_generation.append(mutate(offspring2, adjustment_probability, num_machines))

        population = next_generation[:job_schedule_pool_size]

    best_individual = max(population, key=lambda ind: fitness_function(ind, task_durations, num_machines))
    best_makespan = -fitness_function(best_individual, task_durations, num_machines)

    results.append("\nOptimal Schedule Found:")
    for task, machine in enumerate(best_individual):
        results.append(f"Task {task + 1} -> Machine {machine + 1}")
    results.append(f"\nMinimum Makespan: {best_makespan}")

    return results, best_individual, best_makespan

def run_genetic_algorithm():
    try:
        num_tasks = int(task_count_entry.get())
        num_machines = int(machine_count_entry.get())
        task_durations = list(map(int, task_durations_entry.get().split()))
        job_schedule_pool_size = int(population_size_entry.get())
        iteration_limit = int(generation_count_entry.get())
        adjustment_probability = float(mutation_rate_entry.get())

        if len(task_durations) != num_tasks:
            raise ValueError("Number of task durations does not match the number of tasks.")

        results, _, _ = genetic_algorithm_job_scheduling(
            job_schedule_pool_size, task_durations, num_machines, iteration_limit, adjustment_probability
        )

        results_text.delete(1.0, tk.END)
        results_text.insert(tk.END, "\n".join(results))

    except ValueError as e:
        messagebox.showerror("Invalid Input", str(e))

# Create the GUI
root = tk.Tk()
root.title("Job Scheduling Optimizer")
root.configure(bg="#f3e5f5")  # Light purple background

# Style Configuration
style = ttk.Style()
style.configure("TLabel", font=("Helvetica", 10), background="#f3e5f5")
style.configure("TButton", font=("Helvetica", 10), background="#d1c4e9")

# Input labels and fields
ttk.Label(root, text="Number of Tasks:").grid(row=0, column=0, padx=10, pady=5, sticky=tk.W)
task_count_entry = ttk.Entry(root)
task_count_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Number of Machines:").grid(row=1, column=0, padx=10, pady=5, sticky=tk.W)
machine_count_entry = ttk.Entry(root)
machine_count_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="Task Durations (space-separated):").grid(row=2, column=0, padx=10, pady=5, sticky=tk.W)
task_durations_entry = ttk.Entry(root)
task_durations_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(root, text="Population Size:").grid(row=3, column=0, padx=10, pady=5, sticky=tk.W)
population_size_entry = ttk.Entry(root)
population_size_entry.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(root, text="Number of Generations:").grid(row=4, column=0, padx=10, pady=5, sticky=tk.W)
generation_count_entry = ttk.Entry(root)
generation_count_entry.grid(row=4, column=1, padx=10, pady=5)

ttk.Label(root, text="Mutation Rate (e.g., 0.01 for 1%):").grid(row=5, column=0, padx=10, pady=5, sticky=tk.W)
mutation_rate_entry = ttk.Entry(root)
mutation_rate_entry.grid(row=5, column=1, padx=10, pady=5)

# Run button
run_button = ttk.Button(root, text="Run Optimization", command=run_genetic_algorithm)
run_button.grid(row=6, column=0, columnspan=2, pady=10)

# Results display
ttk.Label(root, text="Results:").grid(row=7, column=0, padx=10, pady=5, sticky=tk.W)
results_text = tk.Text(root, height=15, width=50, bg="#ede7f6", font=("Helvetica", 10))  # Purple tint background
results_text.grid(row=8, column=0, columnspan=2, padx=10, pady=5)

# Heading styling
header_label = tk.Label(root, text="Job Scheduling Optimizer", font=("Helvetica", 16, "bold", "underline"), bg="#f3e5f5")
header_label.grid(row=9, column=0, columnspan=2, pady=10)

# Start the GUI loop
root.mainloop()