import random

class Match:
    def __init__(self, id, players, guild):
        self.id = id
        self.guild = guild
        self.sorted = False
        self.players = players # List
        self.number_of_players = len(self.players)
        self.host = self.players[random.randint(0, self.number_of_players-1)]
        self.team_1 = []
        self.team_2 = []
        self.votes = {}
        self.modes = { # TODO: make modes of maps instead of maps of modes
            "Live Fire": ['Slayer', 'Odd Ball', 'Strongholds'],
            "Recahrge": ['Slayer', 'Odd Ball', 'Strongholds'],
            "Streets": ['Slayer', 'Odd Ball', 'Strongholds'],
            "Aquarius": ['CTF', 'Slayer'],
            "Bazaar": ['CTF', 'Slayer']
        }
    
# Vote processing methods -------------------------------------------------
    def add_vote(self, player, vote_type):
        already_voted = False

        if player in self.votes:
            already_voted = True   

        self.votes.update({player:vote_type})
        return already_voted

    def recorded_voters(self):
        voter_list = []

        for player in self.players:
            if player in self.votes:
                voter_list.append(player)

        return voter_list

    def missing_voters(self):
        missing_list = []

        for player in self.players:
            if not player in self.votes:
                missing_list.append(player)

        return missing_list

    def count_votes(self, queue_max):        
        vote_tally = {
            'r_count': 0,
            'c_count': 0,
            'b_count': 0,
            'o_count': 0
        }

        for vote in self.votes.values():
            if vote == 'random':
                vote_tally.update({'r_count': vote_tally['r_count']+1})
            elif vote == 'captains':
                vote_tally.update({'c_count': vote_tally['c_count']+1})
            elif vote == 'balance':
                vote_tally.update({'b_count': vote_tally['b_count']+1})
            elif vote == 'ordered':
                vote_tally.update({'o_count': vote_tally['o_count']+1})

        for tally in vote_tally:
            if vote_tally[tally] >= self.number_of_players/2:
                if tally == 'r_count':
                    self.randomize()
                elif tally == 'c_count':
                    self.captains()
                elif tally == 'b_count':
                    self.balance()
                elif tally == 'o_count':
                    self.ordered()
                
                return True

        # Find the largest value (always returns the first highest instance of the max number)
        vote_win = max(vote_tally, key=vote_tally.get)
        max_value = vote_tally[vote_win]

        # Checks to see if there is a tie for the largest number of votes (See comment above for why)
        max_counter = 0
        for vote in vote_tally.values():
            if vote == max_value:
                max_counter += 1

        # Will result in "True" if a tie was found
        if max_counter > 1:
            # NOTE: Randomize winning results
            return False

        # Call method for winning selection mode
        if vote_win == 'r_count':
            self.randomize()
        elif vote_win == 'c_count':
            self.captains()
        elif vote_win == 'b_count':
            self.balance()
        elif vote_win == 'o_count':
            self.ordered()
        
        return True
    
# Selection mode commands -------------------------------------------------
    def randomize(self):
        unsorted_players = self.players.copy()
        for i in range(int(self.number_of_players/2)):
            self.team_1.append(unsorted_players.pop(random.randint(0, len(unsorted_players)-1)))
            self.team_2.append(unsorted_players.pop(random.randint(0, len(unsorted_players)-1)))
        self.sorted = True

    def captains(self):
        # Randomly select 2 captains from player list
        # learn how to dm captins
        # they react with who they want (or respond)
        self.sorted = True

    # Assign teams based on their combined mmr
    def balance(self):
        # TODO: Write algorithm to balance total mmr
        # NOTE: Cannot be completed until the server mmr is saved to a DB
        self.sorted = True

    # Assign teams based on the order they joined the queue
    def ordered(self):
        for i in range(0, (self.number_of_players/2)):
            self.team_1.append(players[i])

        for i in range(self.number_of_players/2, self.number_of_players):
            self.team_2.append(players[i])

        self.sorted = True