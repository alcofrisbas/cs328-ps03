import os
import sys
import random
import csv
"""Module for working with the animal-feature dataset.
"""

def load_name_data(filename):
    '''
    Loads a file with animal names or features.
    Returns the results as a list.
    Parameters:
    filename: name of the file where the animal names/features are stored
    '''
    names = []
    f = open(filename)
    for line in f:
        names.append(line.strip())
    f.close()
    return names
    
def load_animal_feature_data(filename):
    '''
    Loads a file with a binary matrix of animal-feature pairs.
    Each row represents one animal, and each column represents one feature.
    Returns a 2-dimensional list where each inner list is one row in the
    original matrix
    Parameters:
    filename: name of the file where the matrix is stored
    '''
    matrix = []
    f = open(filename)
    for line in f:
        features = []
        split_line = line.split()
        for item in split_line:
            features.append(int(item.strip()))
        matrix.append(features)
    f.close()
    return matrix
        
def play_game(animal_name_file, feature_name_file, matrix_file):
    '''
    Plays 5 guessing games with a human, with varying numbers of
    animals to guess from.
    
    Parameters:
    animal_name_file - name of the file containing names of the possible animals
    feature_name_file - name of the file containing features of the animals
    matrix_file: name of the file where the animal-feature matrix is stored
    '''
    animal_names = load_name_data(animal_name_file)
    feature_names = load_name_data(feature_name_file)
    feature_matrix = load_animal_feature_data(matrix_file)
    
    hypothesis_sizes = [2, 4, 8, 16, 32]
    hyp_size_indices = [i for i in range(len(hypothesis_sizes))]
    random.shuffle(hyp_size_indices)
    num_trials = [0]*len(hypothesis_sizes)
    for index in hyp_size_indices:
        num_trials[index] =  run(human_query, animal_names, feature_names, feature_matrix, hypothesis_sizes[index], sys.stdout)
        
    print("Total trials per game: {}".format(num_trials))
    print("Saving trial data to 'data/my_trial_data.txt'")
    save_trial_data(num_trials, "data/my_trial_data.txt")
    return num_trials

def save_trial_data(trial_list, out_file_name):
    '''Saves the numbers in trial list to the file out_file_name.
    Resulting file is comma separated. If list is 2-d, saves 
    such that each inner list is a comma separated row.
    '''
    if len(trial_list) != 0:
        f = open(out_file_name,"w")
        if isinstance(trial_list[0], int): 
            # 1-d list
            row = ",".join(str(i) for i in trial_list)
            f.write(row)
        else:
            # assume 2-d list
            for trial_set in trial_list:
                row = ",".join(str(i) for i in trial_set)
                f.write(row)
                f.write("\n")
        f.close()
    

def human_query(features, animals, animal_names=None, feature_names=None, feature_matrix=None, known_features=None):
    '''Prompts the player for a guess after showing them
    the input features and animals.
    
    Parameters:
    features - list of features of the target animal
    animals - list of possibilities for the target animal
    (remaining four parameters are included only to make the query function
    for human players and all computer players equivalent in their parameters)
    '''
    print("Features: {}".format(features))
    print("Animals: {}".format(animals))
    animal_guess = input("Your guess: ")
    while animal_guess not in animals:
        print("Invalid guess '{}' (did you make a typo?)".format(
            animal_guess))
        animal_guess = input("Your guess: ")
    return animal_guess  


        
def run(query_fn, animal_names, feature_names, feature_matrix, hyp_size, stream):
    '''Runs one instance of the animal guessing game. Returns the number of
    guesses until the player was correct.
    
    Parameters:
    query_fn - function to call to get the player's guess (may be human or computer player)
    animal_names - list of animal names
    feature_names - list of feature names
    feature_matrix - animal-feature matrix
    hyp_size - number of animals included as possibilities to guess
    stream - where to write output (sys.stdout writes to standard out)
    '''
    # Choose animals in the hypothesis set and the target animal
    animal_choices = random.sample(range(len(animal_names)), hyp_size)
    animals = [animal_names[i] for i in animal_choices]
    animal_index = random.choice(animal_choices)
    animal_name = animal_names[animal_index]
    
    # Make a list of all features we can show to the player
    animal_features = feature_matrix[animal_index]
    valid_features = []
    for i in range(len(animal_features)):
        if animal_features[i]:
            valid_features.append(feature_names[i])
    
    
    # Randomize choice order
    
    random.shuffle(animals)
    random.shuffle(valid_features)

    # Play until guessed
    guessed = False
    num_guesses = 0
    stream.write("-" * 70 + "\n")
    while not guessed:
        animal_guess = query_fn(valid_features[:2 + num_guesses], animals, animal_names, feature_names, feature_matrix)
        if animal_guess == animal_name:
            stream.write("Correct!\n")
            guessed = True
        else:
            stream.write("Sorry, try again.\n")
              
        stream.write("\n")
        num_guesses += 1
           
    return num_guesses
    

    