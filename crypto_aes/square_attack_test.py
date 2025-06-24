import binascii
import numpy as np 


def delta_set(inactive):
    base_state = np.full((4, 4), inactive)
    delta_set = []
    for i in range(256):
        state = base_state.copy()
        state[0, 0] = i
        delta_set.append(state)
    return delta_set

def reverse_state(guess, position, encrypted_ds):
    r = []
    i, j = position
    for s in encrypted_ds:
        inv_add_round_key = s[i, j] ^ guess
        #inv_shift_row sert à rien car le shift ne changera par les valeurs
        inv_sub_byte = REVERSED_S_BOX[inv_add_round_key]
        r.append(before_sub_byte)
    return r


def check_guess_correctness(reversed_bytes)
    r = 0
    for i in reversed_bytes:
        r ^= i
    return r == 0

def guess_byte_at_position(encrypted_delta_sets, position) :
    position_in_state = (position % 4, position // 4)
    for encrypted_delta_set in encrypted_delta_sets:
        correct_guesses = []
        for guess in range(0x100):
            reversed_bytes = reverse_state(guess, position_in_state, encrypted_delta_set)
            if is_guess_correct(reversed_bytes):
                correct_guesses.append(guess)
        if len(correct_guesses) == 1:
            break
    else:
        raise RuntimeError(f"Could not find byte for position {position}")
    return correct_guesses[0]

