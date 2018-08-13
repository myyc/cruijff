# madness

types = {
    1: {
        'desc': 'Any pass attempted from one player to another - free kicks, '
                'corners, throw-ins, goal kicks and goal assists',
        'name': 'Pass'},
    2: {
        'desc': 'Attempted pass made to a player who is in an offside '
                'position',
        'name': 'Offside Pass'},
    3: {
        'desc': "Attempted dribble past an opponent (excluding when "
                "qualifier 211 is present as this is 'overrun' and is not "
                "always a duel event)",
        'name': 'Take On'},
    4: {
        'desc': 'This event ID shown when a foul is committed resulting in a '
                'free kick',
        'name': 'Foul'},
    5: {
        'desc': 'Shown each time the ball goes out of play for a throw-in or '
                'goal kick',
        'name': 'Out'},
    6: {'desc': 'Ball goes out of play for a corner kick',
        'name': 'Corner Awarded'},
    7: {
        'desc': 'Tackle = dispossesses an opponent of the ball - Outcome 1 = '
                'win & retain possession or out of play, 0 = win tackle but '
                'not possession',
        'name': 'Tackle'},
    8: {
        'desc': 'When a player intercepts any pass event between opposition '
                'players and prevents the ball reaching its target. Cannot '
                'be a clearance.',
        'name': 'Interception'},
    10: {
        'desc': 'Goalkeeper event; saving a shot on goal. Can also be an '
                'outfield player event with qualifier 94 for blocked shot.',
        'name': 'Save'},
    11: {'desc': 'Goalkeeper event; catching a crossed ball',
         'name': 'Claim'},
    12: {
        'desc': 'Player under pressure hits ball clear of the defensive zone '
                'or/and out of play',
        'name': 'Clearance'},
    13: {'desc': 'Any shot on goal which goes wide or over the goal',
         'name': 'Miss'},
    14: {'desc': 'Whenever the ball hits the frame of the goal',
         'name': 'Post'},
    15: {
        'desc': 'Shot saved - this event is for the player who made the '
                'shot. Qualifier 82 can be added for blocked shot.',
        'name': 'Attempt Saved'},
    16: {'desc': 'All goals', 'name': 'Goal'},
    17: {
        'desc': 'Bookings - will have red, yellow or 2nd yellow qualifier '
                'plus a reason',
        'name': 'Card'},
    18: {'desc': 'Player is substituted off', 'name': 'Player Off'},
    19: {'desc': 'Player comes on as a substitute', 'name': 'Player on'},
    20: {
        'desc': 'Player is forced to leave the pitch due to injury and the '
                'team have no substitutions left',
        'name': 'Player retired'},
    21: {'desc': 'Player comes back on the pitch',
         'name': 'Player returns'},
    22: {'desc': 'When an outfield player has to replace the goalkeeper',
         'name': 'Player becomes goalkeeper'},
    23: {'desc': 'Goalkeeper becomes an outfield player',
         'name': 'Goalkeeper becomes player'},
    24: {'desc': 'Change in playing conditions',
         'name': 'Condition change'},
    25: {'desc': 'Referee or linesman is replaced',
         'name': 'Official change'},
    27: {
        'desc': 'Used when there is a stoppage in play such as a player '
                'injury',
        'name': 'Start delay'},
    28: {'desc': 'Used when the stoppage ends and play resumes',
         'name': 'End delay'},
    30: {'desc': 'End of a match period', 'name': 'End'},
    32: {'desc': 'Start of a match period', 'name': 'Start'},
    34: {
        'desc': 'Team line up - qualifiers 30, 44, 59, 130, 131 will show '
                'player line up and formation',
        'name': 'Team set up'},
    35: {
        'desc': 'Player moved to a different position but the team formation '
                'remained the same',
        'name': 'Player changed position'},
    36: {
        'desc': 'Player is forced to change jersey number, qualifier will '
                'show the new number',
        'name': 'Player changed Jersey number'},
    37: {
        'desc': 'Event 30 signals end of half. This signals end of the match '
                'and thus data collection.',
        'name': 'Collection End'},
    38: {
        'desc': 'Goal has occurred but it is pending additional detail '
                'qualifiers from Opta. Will change to event 16.',
        'name': 'Temp_Goal'},
    39: {
        'desc': 'Shot on goal has occurred but is pending additional detail '
                'qualifiers from Opta. Will change to event 15.',
        'name': 'Temp_Attempt'},
    40: {'desc': 'Team alters its formation', 'name': 'Formation change'},
    41: {'desc': 'Goalkeeper event; ball is punched clear',
         'name': 'Punch'},
    42: {'desc': 'A player shows a good piece of skill on the ball – such as '
                 'a step over or turn on the ball',
         'name': 'Good Skill'},
    43: {
        'desc': 'Event has been deleted – the event will remain as it was '
                'originally with the same ID but will be resent with the type '
                'altered to 43.',
        'name': 'Deleted event'},
    44: {
        'desc': 'Aerial duel – 50/50 when the ball is in the air – outcome '
                'will represent whether the duel was won or lost',
        'name': 'Aerial'},
    45: {
        'desc': 'When a player fails to win the ball as an opponent '
                'successfully dribbles past them',
        'name': 'Challenge'},
    47: {
        'desc': 'This can occur post match if the referee rescinds a card he '
                'has awarded',
        'name': 'Rescinded card'},
    49: {
        'desc': 'Team wins the possession of the ball and successfully keeps '
                'possession for at least two passes or an attacking play',
        'name': 'Ball recovery'},
    50: {
        'desc': 'Player is successfully tackled and loses possession of the '
                'ball',
        'name': 'Dispossessed'},
    51: {
        'desc': 'Mistake by player losing the ball. Leads to a shot or goals '
                'as described with qualifier 169 or 170',
        'name': 'Error'},
    52: {'desc': 'Goalkeeper event; picks up the ball',
         'name': 'Keeper pick-up'},
    53: {'desc': 'Goalkeeper event; cross not successfully caught',
         'name': 'Cross not claimed'},
    54: {
        'desc': 'Goalkeeper event; comes out and covers the ball in the box '
                'winning possession',
        'name': 'Smother'},
    55: {
        'desc': 'Awarded to last defender when an offside decision is given '
                'against an attacker',
        'name': 'Offside provoked'},
    56: {
        'desc': 'Defender uses his body to shield the ball from an opponent '
                'as it rolls out of play',
        'name': 'Shield ball opp'},
    57: {
        'desc': 'A throw-in not taken correctly resulting in the throw being '
                'awarded to the opposing team',
        'name': 'Foul throw-in'},
    58: {'desc': 'Goalkeeper event; penalty by opposition',
         'name': 'Penalty faced'},
    59: {
        'desc': 'When keeper comes off his line and/or out of his box to '
                'clear the ball',
        'name': 'Keeper Sweeper'},
    60: {
        'desc': 'Used when a player does not actually make a shot on goal '
                'but was in a good position to score and only just missed '
                'receiving a pass',
        'name': 'Chance missed'},
    61: {
        'desc': 'Used when a player makes a bad touch on the ball and loses '
                'possession. Outcome 1 – ball simply hit the player '
                'unintentionally. Outcome 0 – Player unsuccessfully '
                'controlled the ball.',
        'name': 'Ball touch'},
    63: {
        'desc': 'An event indicating a save has occurred but without full '
                'details. Event 10 will follow shortly afterwards with full '
                'details.',
        'name': 'Temp_Save'},
    64: {
        'desc': 'Match resumes on a new date after being abandoned mid game',
        'name': 'Resume'},
    65: {
        'desc': 'Any major talking point or error made by the referee – '
                'decision will be assigned to the relevant team',
        'name': 'Contentious referee decision'},
    66: {'desc': 'Possession event will appear every 5 mins',
         'name': 'Possession Data'},
    67: {
        'desc': 'New duel - 2 players running for a loose ball - GERMAN '
                'ONLY. Outcome 1 or 0.',
        'name': '50/50'},
    68: {
        'desc': 'Delay - ref stops - this to event given to both teams on '
                'restart. No Outcome',
        'name': 'Referee Drop Ball'},
    69: {
        'desc': 'New duel (put through-Q266 is the winning duel event). '
                'Attempt to block a shot or pass - challenge lost',
        'name': 'Failed to Block'},
    70: {'desc': 'Injury Time awarded by Referee',
         'name': 'Injury Time Announcement'},
    71: {'desc': 'Coach Type; 1,2,18,30,32,54,57,58,59',
         'name': 'Coach Setup'},
    72: {
        'desc': 'New event to just show player who is offside instead of '
                'offside pass event',
        'name': 'Caught Offside'},
    73: {
        'desc': 'This is an automated extra event for DFL. It comes with a '
                'tackle or an interception and indicates if the player who '
                'made the tackle/interception retained the ball after this '
                'action or if the tackle/interception was a single ball '
                'touch (other ball contact with type “interception”, '
                'type “Defensive Clearance” or type “ TackleRetainedBall”).',
        'name': 'Other Ball Contact'},
    74: {
        'desc': 'Similar to interception but player already very close to '
                'ball',
        'name': 'Blocked Pass'},
    76: {'desc': 'The match has had an early end', 'name': 'Early end'},
    77: {'desc': 'Event indicating that a player is now off the pitch',
         'name': 'Player Off Pitch'}
}

qual = {
    1: {'desc': 'Long pass over 32 metres', 'name': 'Long ball', 'values': ''},
    2: {'desc': 'A ball played in from wide areas into the box',
        'name': 'Cross',
        'values': ''},
    3: {'desc': 'Pass made with a players head',
        'name': 'Head pass',
        'values': ''},
    4: {
        'desc': 'Ball played through for player making an attacking run to '
                'create a chance on goal',
        'name': 'Through ball',
        'values': ''},
    5: {'desc': 'Any free kick; direct or indirect',
        'name': 'Free kick taken',
        'values': ''},
    6: {
        'desc': 'All corners. Look for qualifier 6 but excluding qualifier 2 '
                'for short corners',
        'name': 'Corner taken',
        'values': ''},
    7: {'desc': 'Player who was in an offside position when pass was made.',
        'name': 'Players caught offside',
        'values': 'Players caught offside'},
    8: {'desc': 'Pass led to a goal disallowed for a foul or offside',
        'name': 'Goal disallowed',
        'values': ''},
    9: {
        'desc': 'When attempt on goal was a penalty kick. ALSO used on Event '
                'type 4 to indicate a penalty was awarded',
        'name': 'Penalty',
        'values': ''},
    10: {'desc': 'Handball', 'name': 'Hand', 'values': ''},
    11: {
        'desc': 'Goalkeeper held onto the ball longer than 6 seconds '
                'resulting in a free kick',
        'name': '6-seconds violation',
        'values': ''},
    12: {'desc': 'A foul due to dangerous play',
         'name': 'Dangerous play',
         'values': ''},
    13: {'desc': 'All fouls', 'name': 'Foul', 'values': ''},
    14: {
        'desc': 'When a player makes a defensive action and they are the last '
                'person between the opponent and the goal',
        'name': 'Last line',
        'values': ''},
    15: {
        'desc': 'Any event where the player used their head such as a shot or '
                'a clearance',
        'name': 'Head',
        'values': ''},
    16: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Small box-centre',
         'values': ''},
    17: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Box-centre',
         'values': ''},
    18: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Out of box-centre',
         'values': ''},
    19: {'desc': 'Zone of the pitch - See appendix 3',
         'name': '35+ centre',
         'values': ''},
    20: {'desc': 'Player shot with right footed',
         'name': 'Right footed',
         'values': ''},
    21: {
        'desc': 'Shot was neither via a player’s head or foot for example '
                'knee or chest',
        'name': 'Other body part',
        'values': ''},
    22: {'desc': 'Shot during open play as opposed to from a set play',
         'name': 'Regular play',
         'values': ''},
    23: {'desc': 'Shot occurred following a fast break situation',
         'name': 'Fast break',
         'values': ''},
    24: {'desc': 'Shot occurred from a crossed free kick',
         'name': 'Set piece',
         'values': ''},
    25: {'desc': 'Shot occurred from a corner',
         'name': 'From corner',
         'values': ''},
    26: {'desc': 'Shot occurred directly from a free kick',
         'name': 'Free kick',
         'values': ''},
    28: {
        'desc': 'Own goal . Note: Use the inverse coordinates of the goal '
                'location',
        'name': 'Own goal',
        'values': ''},
    29: {
        'desc': 'Indicates that there was a pass (assist) from another player '
                'to set up the goal opportunity',
        'name': 'Assisted',
        'values': ''},
    30: {
        'desc': 'This will show all players in the starting line up and '
                'available as a substitute',
        'name': 'Involved',
        'values': "Player ID's in line up"},
    31: {'desc': 'Player shown a yellow card',
         'name': 'Yellow Card',
         'values': ''},
    32: {
        'desc': 'Player receives a 2nd yellow card which automatically '
                'results in a red card',
        'name': 'Second yellow',
        'values': ''},
    33: {'desc': 'Player shown a straight red card',
         'name': 'Red card',
         'values': ''},
    34: {'desc': 'Card shown to player because of abuse to the referee',
         'name': 'Referee abuse',
         'values': ''},
    35: {'desc': 'Card shown to player because of an argument',
         'name': 'Argument',
         'values': ''},
    36: {'desc': 'Card shown to player because of violent conduct.',
         'name': 'Violent conduct',
         'values': ''},
    37: {'desc': 'Card shown to player for time wasting',
         'name': 'Time wasting',
         'values': ''},
    38: {'desc': 'Card shown to player for excessively celebrating a goal',
         'name': 'Excessive celebration',
         'values': ''},
    39: {
        'desc': 'Card shown to player because of contact or communication '
                'with the crowd',
        'name': 'Crowd interaction',
        'values': ''},
    40: {'desc': 'Card shown for unknown reason',
         'name': 'Other reason',
         'values': ''},
    41: {'desc': 'Player off pitch due to injury',
         'name': 'Injury',
         'values': ''},
    42: {'desc': 'Substitution, event 18 for tactical reasons',
         'name': 'Tactical',
         'values': ''},
    44: {
        'desc': 'Goalkeeper, Defender, Midfielder, Forward or Substitute. '
                'These are the playing positions associated with each player '
                'for the specific match they',
        'name': 'Player position',
        'values': 'Dynamic'},
    46: {'desc': 'Wind, rain, fog, snow/hail',
         'name': 'Conditions',
         'values': '1, 2, 3, 4'},
    47: {
        'desc': 'Water logged pitch, wet pitch, damp pitch, normal pitch, dry',
        'name': 'Field Pitch',
        'values': '1, 2, 3, 4, 5'},
    48: {'desc': 'Flood lights, bad visibility, natural lights',
         'name': 'Lightings',
         'values': '1, 2, 3'},
    49: {'desc': 'Number of people in crowd',
         'name': 'Attendance Figure',
         'values': 'Dynamic'},
    50: {'desc': 'Referee, Linesman#1, Linesman#2, Forth official',
         'name': 'Official position',
         'values': '1, 2, 3, 4'},
    51: {'desc': 'Unique ID for the official',
         'name': 'Official ID',
         'values': 'Official ID'},
    53: {
        'desc': 'ID of the player who is injured and causing a delay in the '
                'game',
        'name': 'Injured player id',
        'values': 'ID of player injured'},
    54: {'desc': 'The relating value that has caused the match to end early',
         'name': 'End cause',
         'values': ''},
    55: {
        'desc': 'This will appear for goals or shots, the related event_id '
                'will be that of the assist and thus show the assisting '
                'player ID',
        'name': 'Related event ID',
        'values': 'Event_id'},
    56: {'values': 'Back, left, centre, right', 'name': 'Zone',
         'desc': 'Zone'},
    57: {
        'desc': "Related to event type 30, 1 indicates when it is the end of "
                "collection (the End event has a period_id = 14, "
                "'Post Game')",
        'name': 'End type',
        'values': '0, 1'},
    59: {
        'desc': 'This will be shown for substitutions, line ups, line up '
                'changes',
        'name': 'Jersey number',
        'values': 'Shirt number of player(s)'},
    60: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Small box-right',
         'values': ''},
    61: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Small box-left',
         'values': ''},
    62: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Box-deep right',
         'values': ''},
    63: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Box-right',
         'values': ''},
    64: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Box-left',
         'values': ''},
    65: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Box-deep left',
         'values': ''},
    66: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Out of box-deep right',
         'values': ''},
    67: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Out of box-right',
         'values': ''},
    68: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Out of box-left',
         'values': ''},
    69: {'desc': 'Zone of the pitch - See appendix 3',
         'name': 'Out of box-deep left',
         'values': ''},
    70: {'desc': 'Zone of the pitch - See appendix 3',
         'name': '35+ right',
         'values': ''},
    71: {'desc': 'Zone of the pitch - See appendix 3',
         'name': '35+ left',
         'values': ''},
    72: {'desc': 'Player shot with their left foot',
         'name': 'Left footed',
         'values': ''},
    73: {'desc': 'Hit the left post or missed left',
         'name': 'Left',
         'values': ''},
    74: {'desc': 'Hit crossbar or missed over', 'name': 'High', 'values': ''},
    75: {'desc': 'Hit right post or missed right', 'name': 'Right',
         'values': ''},
    76: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'Low left',
         'values': ''},
    77: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'High left',
         'values': ''},
    78: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'Low centre',
         'values': ''},
    79: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'High centre',
         'values': ''},
    80: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'Low right',
         'values': ''},
    81: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'High Right',
         'values': ''},
    82: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'Blocked',
         'values': ''},
    83: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'Close left',
         'values': ''},
    84: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'Close right',
         'values': ''},
    85: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'Close high',
         'values': ''},
    86: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'Close left and high',
         'values': ''},
    87: {'desc': 'Zone of the goalmouth - See appendix 2',
         'name': 'Close right and high',
         'values': ''},
    88: {
        'desc': 'Event 11 Claim - Goalkeeper claims possession of a crossed '
                'ball',
        'name': 'High claim',
        'values': ''},
    89: {
        'desc': 'When attacker was clear with no defenders between him and '
                'the goalkeeper (can be associated with 10, 11, 12, 13, 14, '
                '15 or 16)',
        'name': '1 on 1',
        'values': ''},
    90: {
        'desc': 'Event 10 Save; when goalkeeper saves a shot but does not '
                'catch the ball',
        'name': 'Deflected save',
        'values': ''},
    91: {
        'desc': 'Event 10 Save; when goalkeeper saves a shot while diving '
                'but does not catch the ball',
        'name': 'Dive and deflect',
        'values': ''},
    92: {'desc': 'Event 10 Save; when goalkeeper saves a shot and catches it',
         'name': 'Catch',
         'values': ''},
    93: {
        'desc': 'Event 10 Save; when goalkeeper saves a shot while diving '
                'and catches it',
        'name': 'Dive and catch',
        'values': ''},
    94: {'desc': 'Defender blocks an opposition shot. Shown with event 10.',
         'name': 'Def block',
         'values': ''},
    95: {
        'desc': 'Free kick given for an illegal pass to the goalkeeper which '
                'was collected by his hands or picked up',
        'name': 'Back pass',
        'values': ''},
    97: {
        'desc': '26 will be used for shot directly from a free kick. 97 only '
                'used with Opta GoalData (game system 4) but not with full '
                'data.',
        'name': 'Direct free',
        'values': ''},
    100: {'desc': 'Shot blocked on the 6 yard line',
          'name': 'Six yard blocked',
          'values': ''},
    101: {'desc': 'Shot saved on the goal line',
          'name': 'Saved off line',
          'values': ''},
    102: {
        'desc': 'Y Co-ordinate of where a shot crossed goal line - see '
                'Appendix 2',
        'name': 'Goal mouth y co-ordinate',
        'values': '0-100'},
    103: {
        'desc': 'Z Co-ordinate for height at which a shot crossed the goal '
                'line - see Appendix 2',
        'name': 'Goal mouth z co-ordinate',
        'values': '0-100'},
    106: {'desc': 'A pass in the opposition’s half of the pitch',
          'name': 'Attacking Pass',
          'values': ''},
    107: {'desc': 'Throw-in taken', 'name': 'Throw-in', 'values': ''},
    108: {'desc': "Shot on the volley (ball doesn't bounce before the shot)",
          'name': 'Volley',
          'values': ''},
    109: {'desc': 'Shot via overhead kick', 'name': 'Overhead', 'values': ''},
    112: {
        'desc': 'Goal where there was a scramble for possession of the ball '
                'and the defence had an opportunity to clear',
        'name': 'Scramble',
        'values': ''},
    113: {'desc': 'Shot was subjectively classed as strong',
          'name': 'Strong',
          'values': ''},
    114: {'desc': 'Shot was subjectively classed as weak',
          'name': 'Weak',
          'values': ''},
    115: {'desc': 'Shot was rising in the air', 'name': 'Rising',
          'values': ''},
    116: {'desc': 'Shot was dipping towards the ground',
          'name': 'Dipping',
          'values': ''},
    117: {
        'desc': 'Shot was an attempt by the attacker to play the ball over '
                'the goalkeeper and into the goal',
        'name': 'Lob',
        'values': ''},
    120: {
        'desc': 'Shot which swerves to the left - from attackers perspective',
        'name': 'Swerve Left',
        'values': ''},
    121: {
        'desc': 'Shot which swerves to the right - from attackers perspective',
        'name': 'Swerve Right',
        'values': ''},
    122: {'desc': 'Shot which swerves in several directions',
          'name': 'Swerve Moving',
          'values': ''},
    123: {'desc': 'Pass event - goalkeeper throws the ball out',
          'name': 'Keeper Throw',
          'values': ''},
    124: {'desc': 'Pass event – goal kick', 'name': 'Goal Kick', 'values': ''},
    127: {
        'desc': 'Related to event type 32, this signifies the actual '
                'direction of play in relation to the TV cameras. X/Y '
                'coordinates however are ALWAYS normalized to Left to Right.',
        'name': 'Direction of Play',
        'values': ''},
    128: {'desc': 'Clearance by goalkeeper where he punches the ball clear',
          'name': 'Punch',
          'values': ''},
    130: {'desc': 'See appendix 4',
          'name': 'Team formation',
          'values': 'Formation ID'},
    131: {'desc': "Player position within a formation - 'See appendix 4",
          'name': 'Team player formation',
          'values': '1 to 11'},
    132: {'desc': 'Free kick or card event; player penalised for simulation',
          'name': 'Dive',
          'values': ''},
    133: {'desc': 'Shot deflected off another player',
          'name': 'Deflection',
          'values': ''},
    136: {
        'desc': 'Goal where the goalkeeper got a touch on the ball as it '
                'went in',
        'name': 'Keeper Touched',
        'values': ''},
    137: {
        'desc': 'Shot going wide or over the goal but still collected/saved '
                'by the goalkeeper with event type 15',
        'name': 'Keeper Saved',
        'values': ''},
    138: {'desc': 'Any shot which hits the post or crossbar',
          'name': 'Hit Woodwork',
          'values': ''},
    139: {'desc': 'Shot saved by goalkeeper that was deflected by a defender',
          'name': 'Own Player',
          'values': ''},
    140: {
        'desc': 'The x pitch coordinate for the end point of a pass - See '
                'Appendix 1',
        'name': 'Pass End X',
        'values': '0_100'},
    141: {
        'desc': 'The y pitch coordinate for the end point of a pass - See '
                'Appendix 1',
        'name': 'Pass End Y',
        'values': '0_100'},
    145: {'desc': 'Formation position of a player coming on - see appendix 4',
          'name': 'Formation slot',
          'values': '1 to 11'},
    146: {'desc': 'The x pitch coordinate for where a shot was blocked',
          'name': 'Blocked x co-ordinate',
          'values': ''},
    147: {'desc': 'The y pitch coordinate for where a shot was blocked',
          'name': 'Blocked y co-ordinate',
          'values': ''},
    152: {'desc': 'A direct free kick.', 'name': 'Direct', 'values': ''},
    153: {'desc': 'Shot missed which does not pass the goal line',
          'name': 'Not past goal line',
          'values': ''},
    154: {
        'desc': 'Shot from an intentional assist i.e. The assisting player '
                'intended the pass, no deflection etc',
        'name': 'Intentional assist',
        'values': ''},
    155: {'desc': 'Pass which was chipped into the air',
          'name': 'Chipped',
          'values': ''},
    156: {
        'desc': 'Pass where player laid the ball into the path of a '
                'teammates run',
        'name': 'Lay-off',
        'values': ''},
    157: {
        'desc': 'Pass played from a player’s own half up towards front '
                'players. Aimed to hit a zone rather than a specific player',
        'name': 'Launch',
        'values': ''},
    158: {'desc': 'Card shown to player for persistent fouls',
          'name': 'Persistent infringement',
          'values': ''},
    159: {'desc': 'Card shown for player using foul language',
          'name': 'Foul and abusive language',
          'values': ''},
    160: {'desc': 'Shot came from a throw-in set piece',
          'name': 'Throw-in set piece',
          'values': ''},
    161: {
        'desc': 'Card shown for player who moves within 10 yards of an '
                'opponent’s free kick',
        'name': 'Encroachment',
        'values': ''},
    162: {'desc': 'Card shown for player leaving the field without permission',
          'name': 'Leaving field',
          'values': ''},
    163: {
        'desc': "Card shown for player entering the field during play "
                "without referee's permission",
        'name': 'Entering field',
        'values': ''},
    164: {'desc': 'Card shown for spitting', 'name': 'Spitting', 'values': ''},
    165: {'desc': 'Card shown for a deliberate tactical foul',
          'name': 'Professional foul last man',
          'values': ''},
    166: {
        'desc': 'Card shown to an outfield player for using their hand to '
                'keep the ball out of the goal',
        'name': 'Professional foul handball',
        'values': ''},
    167: {'desc': 'Tackle or clearance event sent the ball out of play',
          'name': 'Out of play',
          'values': ''},
    168: {
        'desc': 'Pass where a player has "flicked" the ball forward using '
                'their head',
        'name': 'Flick-on',
        'values': ''},
    169: {
        'desc': 'A player error, event 51, which leads to an opponent shot '
                'on goal',
        'name': 'Leading to attempt',
        'values': ''},
    170: {
        'desc': 'A player error, event 51, which lead to an opponent scoring '
                'a goal',
        'name': 'Leading to goal',
        'values': ''},
    171: {'desc': 'Referee rescind a card post match',
          'name': 'Rescinded card',
          'values': ''},
    172: {
        'desc': "Player booked on bench but who hasn't played any minutes in "
                "the match",
        'name': 'No impact on timing',
        'values': ''},
    173: {'desc': 'Goalkeeper save where shot is parried to safety',
          'name': 'Parried safe',
          'values': ''},
    174: {
        'desc': 'Goalkeeper save where shot is parried but only to another '
                'opponent',
        'name': 'Parried danger',
        'values': ''},
    175: {'desc': 'Goalkeeper save using his fingertips',
          'name': 'Fingertip',
          'values': ''},
    176: {'desc': 'Goalkeeper catches the ball', 'name': 'Caught',
          'values': ''},
    177: {'desc': 'Goalkeeper save and collects possession of the ball',
          'name': 'Collected',
          'values': ''},
    178: {'desc': 'Goalkeeper save while standing',
          'name': 'Standing',
          'values': ''},
    179: {'desc': 'Goalkeeper save while diving', 'name': 'Diving',
          'values': ''},
    180: {'desc': 'Goalkeeper saves while stooping',
          'name': 'Stooping',
          'values': ''},
    181: {'desc': 'Goalkeeper save where goalkeeper reaches for the ball',
          'name': 'Reaching',
          'values': ''},
    182: {'desc': 'Goalkeeper saves with his hands',
          'name': 'Hands',
          'values': ''},
    183: {'desc': 'Goalkeeper save using his feet –',
          'name': 'Feet',
          'values': ''},
    184: {
        'desc': 'Card shown when a player does not obey referee instructions',
        'name': 'Dissent',
        'values': ''},
    185: {'desc': 'Blocked cross', 'name': 'Blocked cross', 'values': ''},
    186: {
        'desc': 'Goalkeeper event - shots faced and not saved resulting in '
                'goal',
        'name': 'Scored',
        'values': ''},
    187: {'desc': 'Goalkeeper event - shots faced and saved',
          'name': 'Saved',
          'values': ''},
    188: {
        'desc': 'Goalkeeper event - shot faced which went wide or over. Did '
                'not require a save',
        'name': 'Missed',
        'values': ''},
    190: {
        'desc': 'Used with Event 10. Indicates a shot was saved by the '
                'goalkeeper but in fact the shot was going wide and not on '
                'target',
        'name': 'From shot off target',
        'values': ''},
    191: {
        'desc': 'Foul committed by and on a player who is not in possession '
                'of the ball',
        'name': 'Off the ball foul',
        'values': ''},
    192: {'desc': 'Outfield player blocks a shot with their hand',
          'name': 'Block by hand',
          'values': ''},
    194: {'desc': 'ID of the player who is the team captain',
          'name': 'Captain',
          'values': 'Player ID'},
    195: {
        'desc': 'Player in opposition’s penalty box reaches the by-line and '
                'passes (cuts) the ball backwards to a teammate',
        'name': 'Pull Back',
        'values': ''},
    196: {
        'desc': 'Any pass which crosses the centre zone of the pitch and in '
                'length is greater than 60 on the y axis of the pitch',
        'name': 'Switch of play',
        'values': ''},
    197: {'desc': 'Kit of the team', 'name': 'Team kit', 'values': 'Kit ID'},
    198: {
        'desc': 'Goalkeeper drops the ball on the ground and kicks it long '
                'towards a position rather than a specific player',
        'name': 'GK hoof',
        'values': ''},
    199: {
        'desc': 'Goalkeeper kicks the ball forward straight out of his hands',
        'name': 'Gk kick from hands',
        'values': ''},
    200: {'desc': 'Referee stops play', 'name': 'Referee stop', 'values': ''},
    201: {'desc': 'Delay in play instructed by referee',
          'name': 'Referee delay',
          'values': ''},
    202: {'desc': 'Bad weather stops or interrupts play',
          'name': 'Weather problem',
          'values': ''},
    203: {'desc': 'Trouble within the crowd stops or delays play',
          'name': 'Crowd Trouble',
          'values': ''},
    204: {'desc': 'Fire with the stadium stops or delays play',
          'name': 'Fire',
          'values': ''},
    205: {
        'desc': 'Object throw from the crowd lands on the pitch and delays '
                'play',
        'name': 'Object thrown on pitch',
        'values': ''},
    206: {'desc': 'Spectator comes onto the pitch and forces a delay in play',
          'name': 'Spectator on pitch',
          'values': ''},
    207: {
        'desc': 'Given to an event/delay where the referee still has to make '
                'a decision',
        'name': 'Awaiting officials decision',
        'values': ''},
    208: {'desc': 'Referee sustained injury causing stoppage in play',
          'name': 'Referee injury',
          'values': ''},
    209: {
        'desc': 'Related to event type 30, signifies End event is at the end '
                'of the match',
        'name': 'Game end',
        'values': ''},
    210: {
        'desc': 'The pass was an assist for a shot. The type of shot then '
                'dictates whether it was a goal assist or just key pass.',
        'name': 'Assist',
        'values': ''},
    211: {
        'desc': 'Take on where the player attempting overhits the ball and '
                'it runs away from them out of play or to an opponent',
        'name': 'Overrun',
        'values': ''},
    212: {
        'desc': 'The estimated length the ball has travelled during the '
                'associated event.',
        'name': 'Length',
        'values': 'Dynamic - length of pass in metres'},
    213: {
        'desc': 'The angle the ball travels at during an event relative to '
                'the direction of play. Shown in radians.',
        'name': 'Angle',
        'values': '0 to 6.28 (Radians)'},
    214: {
        'desc': 'Shot was deemed by Opta analysts an excellent opportunity '
                'to score – clear cut chance eg one on one',
        'name': 'Big Chance',
        'values': ''},
    215: {
        'desc': 'Player created the chance to shoot by himself, '
                'not assisted. For example he dribbled to create space for '
                'himself and shot.',
        'name': 'Individual Play',
        'values': ''},
    216: {
        'desc': 'If there was a 2nd assist, i.e a pass to create the '
                'opportunity for the player making the assist. MLS and '
                'German Bundesliga 1 & 2.',
        'name': '2nd related event ID',
        'values': 'Event_id'},
    217: {
        'desc': 'Indicates that this shot had a significant pass to create '
                'the opportunity for the pass which led to a goal',
        'name': '2nd assisted',
        'values': ''},
    218: {
        'desc': 'Pass was deemed a 2nd assist - created the opportunity for '
                'another player to assist a goal',
        'name': '2nd assist',
        'values': ''},
    219: {
        'desc': 'Assigned to event 6 indicating there were defensive players '
                'on both posts when a corner was taken',
        'name': 'Players on both posts',
        'values': ''},
    220: {
        'desc': 'Assigned to event 6 indicating there was a defensive player '
                'on only the near post when a corner was taken',
        'name': 'Player on near post',
        'values': ''},
    221: {
        'desc': 'Assigned to event 6 indicating there was a defensive player '
                'on only the far post when corner was taken',
        'name': 'Player on far post',
        'values': ''},
    222: {
        'desc': 'Assigned to event 6 indicating there were no defensive '
                'players on either post when a corner was taken',
        'name': 'No players on posts',
        'values': ''},
    223: {'desc': 'Corner was crossed into the box swerving towards the goal',
          'name': 'In-swinger',
          'values': ''},
    224: {
        'desc': 'Corner was crossed into the box swerving away from the goal',
        'name': 'Out-swinger',
        'values': ''},
    225: {
        'desc': 'Corner was crossed into the box with a straight ball flight',
        'name': 'Straight',
        'values': ''},
    226: {'desc': 'Match has been suspended',
          'name': 'Match suspended',
          'values': ''},
    227: {'desc': 'Match has resumed', 'name': 'Resume', 'values': ''},
    228: {
        'desc': 'Player blocks an attacking shot unintentionally from their '
                'teammate',
        'name': 'Own Shot Blocked',
        'values': ''},
    229: {
        'desc': 'Opta post match quality control has been completed on this '
                'match',
        'name': 'Post-match complete',
        'values': ''},
    230: {'desc': 'GK position when goal or shot hit post',
          'name': 'GK X Coordinate',
          'values': ''},
    231: {'desc': 'GK position when goal or shot hit post',
          'name': 'GK Y Coordinate',
          'values': ''},
    232: {'desc': 'Goalkeeper smothers ball but is not under any challenge',
          'name': 'Unchallenged',
          'values': ''},
    233: {
        'desc': 'Used for any event where there is the same event for both '
                'teams with outcome 1 or 0. This relates the 2 event '
                'together, for example aerial duels',
        'name': 'Opposite related event ID',
        'values': ''},
    234: {'desc': 'Possession % in last 5 mins',
          'name': 'Home Team Possession',
          'values': ''},
    235: {'desc': 'Possession % in last 5 mins',
          'name': 'Away Team Possession',
          'values': ''},
    236: {
        'desc': 'Similar to interception but player already very close to '
                'ball - instead of touch event in past. Or assigned to the '
                'pass to indicate it was blocked',
        'name': 'Blocked Pass',
        'values': ''},
    237: {'desc': 'Indicates a low goal kick', 'name': 'Low', 'values': ''},
    238: {'desc': 'Ball kicked out of play for injury etc',
          'name': 'Fair Play',
          'values': ''},
    239: {
        'desc': 'Free kick situation blocked by wall – need associated '
                'outfielder hit',
        'name': 'By Wall',
        'values': ''},
    240: {
        'desc': 'Automated qualifier which appears on all GK passes after '
                'keeper collects ball with his hands and then puts it on the '
                'ground.',
        'name': 'GK Start',
        'values': ''},
    241: {'desc': 'Shows if indirect foul is awarded',
          'name': 'Indirect',
          'values': ''},
    242: {'desc': 'Foul committed is for obstruction',
          'name': 'Obstruction',
          'values': ''},
    243: {'desc': 'Card shown for unsporting behaviour',
          'name': 'Unsporting Behaviour',
          'values': ''},
    244: {'desc': 'Card shown for player not retreating at a set-piece',
          'name': 'Not Retreating',
          'values': ''},
    245: {'desc': 'Card shown for player committing a serious foul',
          'name': 'Serious Foul',
          'values': ''},
    246: {'desc': 'Game delayed due to drinks break',
          'name': 'Drinks Break',
          'values': ''},
    247: {'desc': 'Contentious decision relating to offside',
          'name': 'Offside',
          'values': ''},
    248: {
        'desc': 'Contentious decision relating to ball crossing the goal line',
        'name': 'Goal Line',
        'values': ''},
    249: {
        'desc': 'Shot has occurred but it is pending additional detail '
                'qualifiers from Opta.',
        'name': 'Temp_ShotOn',
        'values': ''},
    250: {
        'desc': 'Block has occurred but it is pending additional detail '
                'qualifiers from Opta.',
        'name': 'Temp_Blocked',
        'values': ''},
    251: {
        'desc': 'Shot has hit the post but it is pending additional detail '
                'qualifiers from Opta.',
        'name': 'Temp_Post',
        'values': ''},
    252: {
        'desc': 'Shot has missed but it is pending additional detail '
                'qualifiers from Opta.',
        'name': 'Temp_Missed',
        'values': ''},
    253: {
        'desc': 'Shot has missed but not gone past the end line but it is '
                'pending additional detail qualifiers from Opta.',
        'name': 'Temp_MissNotPassedGoalLine',
        'values': ''},
    254: {'desc': 'A goal followed a dribble by the goalscorer',
          'name': 'Follows a Dribble',
          'values': ''},
    255: {'desc': 'Whether the roof is open',
          'name': 'Open Roof',
          'values': 'Dynamic'},
    256: {'desc': 'Dynamic', 'name': 'Air Humidity', 'values': 'Dynamic'},
    257: {'desc': 'The air pressure',
          'name': 'Air Pressure',
          'values': 'Dynamic'},
    258: {'desc': 'Whether the game is sold out',
          'name': 'Sold Out',
          'values': 'Dynamic'},
    259: {'desc': 'The temperature',
          'name': 'Celsius degrees',
          'values': 'Dynamic'},
    260: {'desc': 'Whether the game is floodlit',
          'name': 'Floodlight',
          'values': 'Dynamic'},
    261: {'desc': 'Goal scored via a 1 on 1 chip over the goalkeeper',
          'name': '1 on 1 Chip',
          'values': ''},
    262: {'desc': 'Goal scored via a back heel',
          'name': 'Back Heel',
          'values': ''},
    263: {'desc': 'Shot or goal directly from a corner',
          'name': 'Direct Corner',
          'values': ''},
    264: {'desc': 'Foul committed aerially', 'name': 'Aerial Foul',
          'values': ''},
    265: {'desc': 'Foul committed by an attempted tackle',
          'name': 'Attempted Tackle',
          'values': ''},
    266: {
        'desc': 'Gets assigned to the defending player who should have '
                'denied the shot. A “put through “ is always linked with a '
                '“failed to block” event on the defending teams side.',
        'name': 'Put Through',
        'values': ''},
    273: {'desc': 'Hit right post after save',
          'name': 'Hit Right Post',
          'values': ''},
    274: {'desc': 'Hit left post after save',
          'name': 'Hit Left Post',
          'values': ''},
    275: {'desc': 'Hit bar after save', 'name': 'Hit Bar', 'values': ''},
    276: {
        'desc': 'Shot missed and went out on the sideline. Please note that '
                'in this context the accompanying Blocked qualifiers (q 147 '
                'and q 153) are where the ball goes out on the touchline.',
        'name': 'Out on sideline',
        'values': ''},
    277: {'desc': 'Number of minutes of injury time given by the referee',
          'name': 'Minutes',
          'values': ''},
    278: {'desc': 'Ball tapped to other player (i.e. for free-kick shot)',
          'name': 'Tap',
          'values': ''},
    279: {'desc': 'Starting pass - to enable exclusion from passing %',
          'name': 'Kick Off',
          'values': 'S = kick-off to start a period (first half, second '
                    'half, first half extra-time, second half extra-time) G '
                    '= kick-off following a goal'},
    280: {
        'desc': 'Related Event to - PASS_LOST, BLOCKED_SHOT, ATTEMPT_SAVED, '
                'POST, FREE_KICK_WON, HANDBALL_WON, OWN_GOAL, PENALTY_WON',
        'name': 'Fantasy Assist Type',
        'values': ''},
    281: {'desc': 'Player making assist',
          'name': 'Fantasy Assisted By',
          'values': ''},
    282: {'desc': 'Team making assist',
          'name': 'Fantasy Assist Team',
          'values': ''},
    283: {'desc': 'ID of the team coach',
          'name': 'Coach ID',
          'values': 'Coach ID'},
    284: {'desc': 'Indicates Blocked Shot is a duel',
          'name': 'Duel',
          'values': ''},
    285: {'desc': 'Indicates a defensive duel',
          'name': 'Defensive',
          'values': ''},
    286: {'desc': 'Indicates an offensive duel',
          'name': 'Offensive',
          'values': ''},
    287: {'desc': 'Indicates over-arm throw out by the goalkeeper',
          'name': 'Over-arm',
          'values': ''},
    288: {
        'desc': 'Amount of time the ball was out of play in the last 5 '
                'minutes',
        'name': 'Out of Play Secs',
        'values': ''},
    289: {
        'desc': 'Foul committed by a player denying a goal-scoring '
                'opportunity',
        'name': 'Denied goal-scoring opp',
        'values': ''},
    290: {'desc': 'Shows Coaches and involved roles',
          'name': 'Coach Types',
          'values': '1,2,18,30,32,54,57,58,59'},
    291: {
        'desc': 'This is an automated extra event for DFL. It comes with a '
                'tackle or an interception and indicates if the player who '
                'made the tackle/interception retained the ball after this '
                'action or if the tackle/interception was a single ball '
                'touch (other ball contact with type “interception”, '
                'type “Defensive Clearance” or type “ TackleRetainedBall).',
        'name': 'Other Ball Contact Type',
        'values': ''},
    294: {'desc': 'Foul given for a shove/push',
          'name': 'Shove/push',
          'values': ''},
    295: {'desc': 'Foul given for shirt pull/holding',
          'name': 'Shirt Pull/Holding',
          'values': ''},
    296: {'desc': 'Foul given for elbow/violent conduct',
          'name': 'Elbow/Violent Conduct',
          'values': ''},
    297: {'desc': 'An offside pass that follwos a rebounded shot',
          'name': 'Follows shot rebound',
          'values': ''},
    298: {'desc': 'An offside pass that follwos a blocked shot',
          'name': 'Follows shot blocked',
          'values': ''},
    299: {
        'desc': 'Related to event types 27 and 28 to indicate the delay is '
                'affecting the match clock',
        'name': 'Clock affecting',
        'values': ''},
    300: {
        'desc': 'Related to event 16 - to show the goal came from a solo run',
        'name': 'Solo run',
        'values': ''},
    301: {
        'desc': 'Related to event type 15 to show it was an attempted save '
                'from a shot that came from a cross',
        'name': 'Shot from cross',
        'values': ''},
    303: {
        'desc': 'Related to event type 303 to show the delay is due to a '
                'floodlight failure',
        'name': 'Floodlight failure',
        'values': ''},
    304: {'desc': 'Player off pitch but ball in play',
          'name': 'Ball In Play',
          'values': ''},
    305: {'desc': 'Ball out of play due to player being off pitch',
          'name': 'Ball Out of Play',
          'values': ''},
    306: {'desc': 'Player off pitch for kit change',
          'name': 'Kit change',
          'values': ''},
    307: {
        'desc': 'The id for phase of possession for DFL. Related to events ('
                '1,2,3,4,7,8,10,11,12,13,14,15,16,41,42,50,54,61,74)',
        'name': 'Phase of posession ID',
        'values': ''},
    308: {'desc': 'Related to event type 30, match has went to extra time',
          'name': 'Goes to extra time',
          'values': ''},
    309: {'desc': 'Related to event type 30, match has gone to penalties',
          'name': 'Goes to penalties',
          'values': ''},
    310: {'desc': 'Player goes out of pitch',
          'name': 'Player goes out',
          'values': ''},
    311: {'desc': 'Player comes back onto pitch',
          'name': 'Player comes back',
          'values': ''},
    312: {
        'desc': 'Indicator that possession has started for DFL. (Related to '
                'events 3,7,8,10,11,54,74)',
        'name': 'Phase of possession start',
        'values': ''},
    313: {'desc': 'Foul given for an illegal restart',
          'name': 'Illegal Restart',
          'values': ''},
    314: {'desc': 'Foul given for shot hitting offside player',
          'name': 'End of offside',
          'values': ''}}

form = {
    2: "442",
    3: "41212",
    4: "433",
    5: "451",
    6: "4411",
    7: "4141",
    8: "4231",
    9: "4321",
    10: "532",
    11: "541",
    12: "352",
    13: "343",
    14: "4222",
    15: "3511",
    16: "3421",
    17: "3412",
    18: "3142",
    19: "343d",
    20: "4132",
    21: "4240",
    22: "4312"
}
