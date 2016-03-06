class DFA_to_REGEX(object):

    def __init__(self, transition_table, q, f, S):
        self.transition_table = transition_table
        self.q = q
        self.f = f
        self.S = S

    def dfa_to_gnfa(self):
        dfa_starting_state = self.q
        dfa_accept_state = self.f
        gnfa = self.transition_table
        gnfa['s'] = {dfa_starting_state: 'e'}
        gnfa['f'] = {'': ''}

        for accept_state in dfa_accept_state:
            gnfa[accept_state]['f'] = 'e'

        return gnfa

    @staticmethod
    def new_transition(qi, el_state, qj, gnfa):

        if el_state in gnfa[qi].keys():
            if gnfa[qi][el_state] != 'e':
                if '*' in gnfa[qi][el_state] or '|' in gnfa[qi][el_state]:
                    r1 = '(' + gnfa[qi][el_state] + ')'
                else:
                    r1 = gnfa[qi][el_state]
            else:
                r1 = ''
        else:
            r1 = ''

        if el_state in gnfa[el_state].keys():
                if '*' in gnfa[el_state][el_state] or '|' in gnfa[el_state][el_state] or len(gnfa[el_state][el_state]) > 1:
                    r2 = '(' + gnfa[el_state][el_state] + ')*'
                else:
                    r2 = gnfa[el_state][el_state] + '*'
        else:
            r2 = ''

        if qj in gnfa[el_state].keys():
                if '*' in gnfa[el_state][qj] or '|' in gnfa[el_state][qj]:
                    r3 = '(' + gnfa[el_state][qj] + ')'
                else:
                    r3 = gnfa[el_state][qj]
        else:
            r3 = ''

        if qj in gnfa[qi].keys():
                if '*' in gnfa[qi][qj] or '|' in gnfa[qi][qj]:
                    r4 = '(' + gnfa[qi][qj] + ')'
                else:
                    r4 = gnfa[qi][qj]
        else:
            r4 = ''
        if r4 != '':
            r3 += '|'

        x = r1 + r2 + r3 + r4

        return x

    @staticmethod
    def main(gnfa, sequence_of_elimination):

        total_states = len(gnfa)

        while total_states > 2:
            for el_state in sequence_of_elimination:

                t = gnfa[el_state].keys()
                f = []
                for q in gnfa:
                    for key in gnfa[q].keys():
                        if key == el_state:
                            f.append(q)

                for qi in f:
                    for qj in t:
                        if qj != el_state and qi != el_state:
                            new_tr = DFA_to_REGEX.new_transition(qi, el_state, qj, gnfa)
                            gnfa[qi][qj] = new_tr

                # state elimination below
                gnfa.pop(el_state)
                for q in gnfa:
                    for key in gnfa[q].keys():
                        if key == el_state:
                            gnfa[q].pop(el_state)
                sequence_of_elimination.pop(sequence_of_elimination.index(el_state))

                DFA_to_REGEX.main(gnfa, sequence_of_elimination)

            return gnfa

    @staticmethod
    def filtering_input(input):
        filt_output = []
        x = input[0]
        for i in range(1, len(input)):
            if input[i] != ',':
                x += input[i]
            else:
                filt_output.append(x)
                x = ''
        if x != '':
            filt_output.append(x)
        return filt_output


if __name__ == '__main__':
    ans = ''
    while ans != 'y' and ans != 'yes' and ans != 'Yes' and ans != 'YES' and ans != 'Y':
        print ''
        print '=============== DFA TO REGEX CONVERTER ==================\n'

        num_state = raw_input("Number of states: ")
        num_state = num_state.replace(" ", "")
        print "The states of the DFA are: "
        for i in range(int(num_state)):
            print i,
        print '\n'

        starting_state = raw_input('starting state: ')
        starting_state = starting_state.replace(" ", "")

        approve_state_input = raw_input("accept states (states are seperated with comma (,) for examble: 2,3,5) \n"
                                        ": ")
        approve_state = DFA_to_REGEX.filtering_input(approve_state_input)
        alphabet = raw_input("give the alphabet (symbols are seperated with comma (,) for example a,b \n"
                             ": ")
        alphabet = alphabet.replace(" ", "")
        alphabet = DFA_to_REGEX.filtering_input(alphabet)
        trans_table = {}

        print ''
        print "transitions from a state to another: "
        for i in range(int(num_state)):
            trans_table[str(i)] = {}
            k = 0
            while k < len(alphabet):
                state = raw_input('from state %d with %s to ' % (i, alphabet[k]))
                state = state.replace(" ", "")
                if state in trans_table[str(i)]:
                    trans_table[str(i)][state] += '|' + alphabet[k]
                else:
                    trans_table[str(i)][state] = alphabet[k]
                k += 1
        print ''

        sequence_of_elimination = raw_input("Give the sequence of states elimination (states are seperated with comma (,) for examble: 0,2,1) \n"
                                            ": ")
        sequence_of_elimination = sequence_of_elimination.replace(" ", "")
        sequence_of_elimination = DFA_to_REGEX.filtering_input(sequence_of_elimination)
        print ''

        print "------- SUMMARISE USERS INPUT -------- "
        print 'Number of states: ', num_state
        print 'Starting state', starting_state
        print 'Accept states', approve_state
        print 'DFA in dictionary format:', trans_table
        print 'Sequence of states elimination: ', sequence_of_elimination
        ans = raw_input("Do you want to proceed? (y/n): ")
        ans = ans.replace(" ", "")
    print ''

    ins = DFA_to_REGEX(trans_table, starting_state, approve_state, alphabet)
    gnfa = DFA_to_REGEX.dfa_to_gnfa(ins)
    last_gnfa = DFA_to_REGEX.main(gnfa, sequence_of_elimination)
    regular_expression = last_gnfa['s']['f']
    print "THE REGULAR EXPRESSION IS -------> ", regular_expression
    print ''
