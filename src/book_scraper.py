"""BookAuthority scraper + curated seed list of canonical social skills books.

Since BookAuthority.org may block automated scraping, we include a manually
curated seed list based on the paper's description: books from Amazon Self-Help
rankings and BookAuthority category rankings that are widely cited in social
skills literature.
"""

from typing import List, Dict


def get_seed_books() -> List[Dict]:
    """Return a curated seed list of canonical social skills books.

    These are the most widely cited and recognized books in social skills
    education, sourced from:
    - Amazon Books Self-Help bestsellers
    - BookAuthority.org category rankings
    - Books explicitly mentioned in the SocialCoach paper

    Each book is tagged with its primary category.
    """
    books = [
        # === Emotional Intelligence ===
        {"title": "Emotional Intelligence: Why It Can Matter More Than IQ", "author": "Daniel Goleman", "isbn": "9780553383713", "publication_year": "1995", "category": "Emotional Intelligence"},
        {"title": "Working with Emotional Intelligence", "author": "Daniel Goleman", "isbn": "9780553378580", "publication_year": "1998", "category": "Emotional Intelligence"},
        {"title": "Social Intelligence: The New Science of Human Relationships", "author": "Daniel Goleman", "isbn": "9780553384499", "publication_year": "2006", "category": "Social Intelligence"},
        {"title": "Emotional Agility: Get Unstuck, Embrace Change, and Thrive in Work and Life", "author": "Susan David", "isbn": "9781592409495", "publication_year": "2016", "category": "Emotional Intelligence"},
        {"title": "Permission to Feel: Unlocking the Power of Emotions to Help Our Kids, Ourselves, and Our Society Thrive", "author": "Marc Brackett", "isbn": "9781250212849", "publication_year": "2019", "category": "Emotional Intelligence"},
        {"title": "The Language of Emotions: What Your Feelings Are Trying to Tell You", "author": "Karla McLaren", "isbn": "9781591797692", "publication_year": "2010", "category": "Emotional Intelligence"},
        {"title": "Emotional Intelligence 2.0", "author": "Travis Bradberry", "isbn": "9780974320625", "publication_year": "2009", "category": "Emotional Intelligence"},
        {"title": "The EQ Edge: Emotional Intelligence and Your Success", "author": "Steven J. Stein", "isbn": "9780470681619", "publication_year": "2011", "category": "Emotional Intelligence"},
        {"title": "Primal Leadership: Unleashing the Power of Emotional Intelligence", "author": "Daniel Goleman", "isbn": "9781422168035", "publication_year": "2013", "category": "Emotional Intelligence"},
        {"title": "The Emotionally Intelligent Manager", "author": "David R. Caruso", "isbn": "9780787970710", "publication_year": "2004", "category": "Emotional Intelligence"},

        # === Communication ===
        {"title": "Nonviolent Communication: A Language of Life", "author": "Marshall B. Rosenberg", "isbn": "9781892005281", "publication_year": "2015", "category": "Communication"},
        {"title": "Crucial Conversations: Tools for Talking When Stakes Are High", "author": "Kerry Patterson", "isbn": "9781260474183", "publication_year": "2021", "category": "Communication"},
        {"title": "How to Win Friends and Influence People", "author": "Dale Carnegie", "isbn": "9780671027032", "publication_year": "1936", "category": "Communication"},
        {"title": "Difficult Conversations: How to Discuss What Matters Most", "author": "Douglas Stone", "isbn": "9780143118442", "publication_year": "2010", "category": "Communication"},
        {"title": "Just Listen: Discover the Secret to Getting Through to Absolutely Anyone", "author": "Mark Goulston", "isbn": "9780814436479", "publication_year": "2015", "category": "Communication"},
        {"title": "Thanks for the Feedback: The Science and Art of Receiving Feedback Well", "author": "Douglas Stone", "isbn": "9780670014668", "publication_year": "2014", "category": "Communication"},
        {"title": "Radical Candor: Be a Kick-Ass Boss Without Losing Your Humanity", "author": "Kim Scott", "isbn": "9781250103505", "publication_year": "2017", "category": "Communication"},
        {"title": "The Coaching Habit: Say Less, Ask More & Change the Way You Lead Forever", "author": "Michael Bungay Stanier", "isbn": "9780978440749", "publication_year": "2016", "category": "Communication"},
        {"title": "Never Split the Difference: Negotiating As If Your Life Depended On It", "author": "Chris Voss", "isbn": "9780062407801", "publication_year": "2016", "category": "Communication"},
        {"title": "Talk Like TED: The 9 Public-Speaking Secrets of the World's Top Minds", "author": "Carmine Gallo", "isbn": "9781250041128", "publication_year": "2014", "category": "Communication"},
        {"title": "You're Not Listening: What You're Missing and Why It Matters", "author": "Kate Murphy", "isbn": "9781250297198", "publication_year": "2020", "category": "Communication"},
        {"title": "Supercommunicators: How to Unlock the Secret Language of Connection", "author": "Charles Duhigg", "isbn": "9780593243916", "publication_year": "2024", "category": "Communication"},

        # === Leadership ===
        {"title": "Leaders Eat Last: Why Some Teams Pull Together and Others Don't", "author": "Simon Sinek", "isbn": "9781591848011", "publication_year": "2014", "category": "Leadership"},
        {"title": "Dare to Lead: Brave Work. Tough Conversations. Whole Hearts.", "author": "Brene Brown", "isbn": "9780399592522", "publication_year": "2018", "category": "Leadership"},
        {"title": "The 7 Habits of Highly Effective People", "author": "Stephen R. Covey", "isbn": "9781982137274", "publication_year": "1989", "category": "Leadership"},
        {"title": "Start with Why: How Great Leaders Inspire Everyone to Take Action", "author": "Simon Sinek", "isbn": "9781591846444", "publication_year": "2009", "category": "Leadership"},
        {"title": "Good to Great: Why Some Companies Make the Leap and Others Don't", "author": "Jim Collins", "isbn": "9780066620992", "publication_year": "2001", "category": "Leadership"},
        {"title": "The Five Dysfunctions of a Team: A Leadership Fable", "author": "Patrick Lencioni", "isbn": "9780787960759", "publication_year": "2002", "category": "Leadership"},
        {"title": "Multipliers: How the Best Leaders Make Everyone Smarter", "author": "Liz Wiseman", "isbn": "9780062663078", "publication_year": "2017", "category": "Leadership"},
        {"title": "Turn the Ship Around!: A True Story of Turning Followers into Leaders", "author": "L. David Marquet", "isbn": "9781591846406", "publication_year": "2013", "category": "Leadership"},
        {"title": "The Servant: A Simple Story About the True Essence of Leadership", "author": "James C. Hunter", "isbn": "9780761513698", "publication_year": "1998", "category": "Leadership"},
        {"title": "Servant Leadership: A Journey into the Nature of Legitimate Power and Greatness", "author": "Robert K. Greenleaf", "isbn": "9780809105540", "publication_year": "2002", "category": "Leadership"},
        {"title": "The 21 Irrefutable Laws of Leadership", "author": "John C. Maxwell", "isbn": "9780785288374", "publication_year": "2007", "category": "Leadership"},
        {"title": "Extreme Ownership: How U.S. Navy SEALs Lead and Win", "author": "Jocko Willink", "isbn": "9781250183866", "publication_year": "2017", "category": "Leadership"},
        {"title": "Tribal Leadership: Leveraging Natural Groups to Build a Thriving Organization", "author": "Dave Logan", "isbn": "9780061251320", "publication_year": "2008", "category": "Leadership"},

        # === Negotiation ===
        {"title": "Getting to Yes: Negotiating Agreement Without Giving In", "author": "Roger Fisher", "isbn": "9780143118756", "publication_year": "2011", "category": "Negotiation"},
        {"title": "Influence: The Psychology of Persuasion", "author": "Robert B. Cialdini", "isbn": "9780062937650", "publication_year": "2021", "category": "Negotiation"},
        {"title": "Pre-Suasion: A Revolutionary Way to Influence and Persuade", "author": "Robert B. Cialdini", "isbn": "9781501109805", "publication_year": "2016", "category": "Negotiation"},
        {"title": "Getting Past No: Negotiating in Difficult Situations", "author": "William Ury", "isbn": "9780553371314", "publication_year": "1993", "category": "Negotiation"},
        {"title": "Bargaining for Advantage: Negotiation Strategies for Reasonable People", "author": "G. Richard Shell", "isbn": "9780143036975", "publication_year": "2006", "category": "Negotiation"},
        {"title": "The Art of Negotiation: How to Improvise Agreement in a Chaotic World", "author": "Michael Wheeler", "isbn": "9781451690439", "publication_year": "2013", "category": "Negotiation"},
        {"title": "Getting More: How You Can Negotiate to Succeed in Work and Life", "author": "Stuart Diamond", "isbn": "9780307716903", "publication_year": "2010", "category": "Negotiation"},
        {"title": "Negotiation Genius: How to Overcome Obstacles and Achieve Brilliant Results", "author": "Deepak Malhotra", "isbn": "9780553384116", "publication_year": "2008", "category": "Negotiation"},
        {"title": "The Mind and Heart of the Negotiator", "author": "Leigh Thompson", "isbn": "9780133571776", "publication_year": "2014", "category": "Negotiation"},

        # === Conflict Resolution ===
        {"title": "Crucial Accountability: Tools for Resolving Violated Expectations", "author": "Kerry Patterson", "isbn": "9780071829311", "publication_year": "2013", "category": "Conflict Resolution"},
        {"title": "The Anatomy of Peace: Resolving the Heart of Conflict", "author": "The Arbinger Institute", "isbn": "9781626564312", "publication_year": "2015", "category": "Conflict Resolution"},
        {"title": "Resolving Conflicts at Work: Ten Strategies for Everyone on the Job", "author": "Kenneth Cloke", "isbn": "9780787980245", "publication_year": "2011", "category": "Conflict Resolution"},
        {"title": "The Third Side: Why We Fight and How We Can Stop", "author": "William Ury", "isbn": "9780140296341", "publication_year": "2000", "category": "Conflict Resolution"},
        {"title": "Fierce Conversations: Achieving Success at Work and in Life One Conversation at a Time", "author": "Susan Scott", "isbn": "9780425193372", "publication_year": "2004", "category": "Conflict Resolution"},
        {"title": "Conflict Resolution for Holy Beings: Poems", "author": "Joy Harjo", "isbn": "9780393353631", "publication_year": "2015", "category": "Conflict Resolution"},
        {"title": "Say What You Mean: A Mindful Approach to Nonviolent Communication", "author": "Oren Jay Sofer", "isbn": "9781611805833", "publication_year": "2018", "category": "Conflict Resolution"},
        {"title": "High Conflict: Why We Get Trapped and How We Get Out", "author": "Amanda Ripley", "isbn": "9781982128562", "publication_year": "2021", "category": "Conflict Resolution"},

        # === Empathy ===
        {"title": "Empathy: Why It Matters, and How to Get It", "author": "Roman Krznaric", "isbn": "9780399171406", "publication_year": "2014", "category": "Empathy"},
        {"title": "Born for Love: Why Empathy Is Essential--and Endangered", "author": "Bruce D. Perry", "isbn": "9780061656798", "publication_year": "2010", "category": "Empathy"},
        {"title": "The War for Kindness: Building Empathy in a Fractured World", "author": "Jamil Zaki", "isbn": "9780451499240", "publication_year": "2019", "category": "Empathy"},
        {"title": "Against Empathy: The Case for Rational Compassion", "author": "Paul Bloom", "isbn": "9780062339348", "publication_year": "2016", "category": "Empathy"},
        {"title": "The Age of Empathy: Nature's Lessons for a Kinder Society", "author": "Frans de Waal", "isbn": "9780307407764", "publication_year": "2009", "category": "Empathy"},
        {"title": "I Know How You Feel: The Joy and Heartbreak of Friendship in Women's Lives", "author": "F. Diane Barth", "isbn": "9780544870345", "publication_year": "2018", "category": "Empathy"},
        {"title": "Self-Compassion: The Proven Power of Being Kind to Yourself", "author": "Kristin Neff", "isbn": "9780061733529", "publication_year": "2011", "category": "Empathy"},
        {"title": "Compassionomics: The Revolutionary Scientific Evidence That Caring Makes a Difference", "author": "Stephen Trzeciak", "isbn": "9781622181063", "publication_year": "2019", "category": "Empathy"},

        # === Relationships ===
        {"title": "Attached: The New Science of Adult Attachment and How It Can Help YouFind and Keep Love", "author": "Amir Levine", "isbn": "9781585429134", "publication_year": "2010", "category": "Relationships"},
        {"title": "The Relationship Cure: A 5 Step Guide to Strengthening Your Marriage, Family, and Friendships", "author": "John M. Gottman", "isbn": "9780609809532", "publication_year": "2001", "category": "Relationships"},
        {"title": "Hold Me Tight: Seven Conversations for a Lifetime of Love", "author": "Sue Johnson", "isbn": "9780316113007", "publication_year": "2008", "category": "Relationships"},
        {"title": "The Five Love Languages: The Secret to Love that Lasts", "author": "Gary Chapman", "isbn": "9780802412706", "publication_year": "2015", "category": "Relationships"},
        {"title": "Set Boundaries, Find Peace: A Guide to Reclaiming Yourself", "author": "Nedra Glennon Tawwab", "isbn": "9780593192092", "publication_year": "2021", "category": "Relationships"},
        {"title": "Boundaries: When to Say Yes, How to Say No to Take Control of Your Life", "author": "Henry Cloud", "isbn": "9780310351801", "publication_year": "2017", "category": "Relationships"},
        {"title": "The Gifts of Imperfection", "author": "Brene Brown", "isbn": "9781592858491", "publication_year": "2010", "category": "Relationships"},
        {"title": "Daring Greatly: How the Courage to Be Vulnerable Transforms the Way We Live", "author": "Brene Brown", "isbn": "9781592408412", "publication_year": "2012", "category": "Relationships"},
        {"title": "The Art of Loving", "author": "Erich Fromm", "isbn": "9780061129735", "publication_year": "1956", "category": "Relationships"},
        {"title": "No More Mr. Nice Guy", "author": "Robert A. Glover", "isbn": "9780762415335", "publication_year": "2003", "category": "Relationships"},
        {"title": "Platonic: How the Science of Attachment Can Help You Make and Keep Friends", "author": "Marisa G. Franco", "isbn": "9780593185544", "publication_year": "2022", "category": "Relationships"},

        # === Self-Awareness ===
        {"title": "Insight: The Surprising Truth About How Others See Us, How We See Ourselves, and Why the Answers Matter More Than We Think", "author": "Tasha Eurich", "isbn": "9780451496676", "publication_year": "2017", "category": "Self-Awareness"},
        {"title": "Thinking, Fast and Slow", "author": "Daniel Kahneman", "isbn": "9780374533557", "publication_year": "2011", "category": "Self-Awareness"},
        {"title": "Mindset: The New Psychology of Success", "author": "Carol S. Dweck", "isbn": "9780345472328", "publication_year": "2006", "category": "Self-Awareness"},
        {"title": "The Power of Now: A Guide to Spiritual Enlightenment", "author": "Eckhart Tolle", "isbn": "9781577314806", "publication_year": "1997", "category": "Self-Awareness"},
        {"title": "Quiet: The Power of Introverts in a World That Can't Stop Talking", "author": "Susan Cain", "isbn": "9780307352156", "publication_year": "2012", "category": "Self-Awareness"},
        {"title": "Man's Search for Meaning", "author": "Viktor E. Frankl", "isbn": "9780807014271", "publication_year": "1946", "category": "Self-Awareness"},
        {"title": "The Four Agreements: A Practical Guide to Personal Freedom", "author": "Don Miguel Ruiz", "isbn": "9781878424310", "publication_year": "1997", "category": "Self-Awareness"},
        {"title": "The Untethered Soul: The Journey Beyond Yourself", "author": "Michael A. Singer", "isbn": "9781572245372", "publication_year": "2007", "category": "Self-Awareness"},
        {"title": "Personality Isn't Permanent: Break Free from Self-Limiting Beliefs and Rewrite Your Story", "author": "Benjamin Hardy", "isbn": "9780593083697", "publication_year": "2020", "category": "Self-Awareness"},

        # === Social Intelligence ===
        {"title": "The Charisma Myth: How Anyone Can Master the Art and Science of Personal Magnetism", "author": "Olivia Fox Cabane", "isbn": "9781591845942", "publication_year": "2012", "category": "Social Intelligence"},
        {"title": "Captivate: The Science of Succeeding with People", "author": "Vanessa Van Edwards", "isbn": "9780399564482", "publication_year": "2017", "category": "Social Intelligence"},
        {"title": "The Like Switch: An Ex-FBI Agent's Guide to Influencing, Attracting, and Winning People Over", "author": "Jack Schafer", "isbn": "9781476754482", "publication_year": "2015", "category": "Social Intelligence"},
        {"title": "What Every BODY is Saying: An Ex-FBI Agent's Guide to Speed-Reading People", "author": "Joe Navarro", "isbn": "9780061438295", "publication_year": "2008", "category": "Social Intelligence"},
        {"title": "Cues: Master the Secret Language of Charismatic Communication", "author": "Vanessa Van Edwards", "isbn": "9780593332184", "publication_year": "2022", "category": "Social Intelligence"},
        {"title": "The Art of People: 11 Simple People Skills That Will Get You Everything You Want", "author": "Dave Kerpen", "isbn": "9780553419405", "publication_year": "2016", "category": "Social Intelligence"},
        {"title": "People Skills: How to Assert Yourself, Listen to Others, and Resolve Conflicts", "author": "Robert Bolton", "isbn": "9780671622480", "publication_year": "1986", "category": "Social Intelligence"},
        {"title": "How to Talk to Anyone: 92 Little Tricks for Big Success in Relationships", "author": "Leil Lowndes", "isbn": "9780071418584", "publication_year": "2003", "category": "Social Intelligence"},
        {"title": "The Science of People: Master Body Language, Behavior, and Communication", "author": "Vanessa Van Edwards", "isbn": "9780399564499", "publication_year": "2017", "category": "Social Intelligence"},

        # === Self-Management ===
        {"title": "Atomic Habits: An Easy & Proven Way to Build Good Habits & Break Bad Ones", "author": "James Clear", "isbn": "9780735211292", "publication_year": "2018", "category": "Self-Management"},
        {"title": "The Power of Habit: Why We Do What We Do in Life and Business", "author": "Charles Duhigg", "isbn": "9780812981605", "publication_year": "2012", "category": "Self-Management"},
        {"title": "Grit: The Power of Passion and Perseverance", "author": "Angela Duckworth", "isbn": "9781501111105", "publication_year": "2016", "category": "Self-Management"},
        {"title": "Drive: The Surprising Truth About What Motivates Us", "author": "Daniel H. Pink", "isbn": "9781594484803", "publication_year": "2009", "category": "Self-Management"},
        {"title": "The Willpower Instinct: How Self-Control Works, Why It Matters, and What You Can Do to Get More of It", "author": "Kelly McGonigal", "isbn": "9781583335086", "publication_year": "2011", "category": "Self-Management"},
        {"title": "Burnout: The Secret to Unlocking the Stress Cycle", "author": "Emily Nagoski", "isbn": "9781984818324", "publication_year": "2019", "category": "Self-Management"},
        {"title": "When the Body Says No: Understanding the Stress-Disease Connection", "author": "Gabor Mate", "isbn": "9780470923351", "publication_year": "2003", "category": "Self-Management"},
        {"title": "The Upside of Stress: Why Stress Is Good for You, and How to Get Good at It", "author": "Kelly McGonigal", "isbn": "9781583335611", "publication_year": "2015", "category": "Self-Management"},
        {"title": "Tiny Habits: The Small Changes That Change Everything", "author": "BJ Fogg", "isbn": "9780358003328", "publication_year": "2019", "category": "Self-Management"},
        {"title": "Deep Work: Rules for Focused Success in a Distracted World", "author": "Cal Newport", "isbn": "9781455586691", "publication_year": "2016", "category": "Self-Management"},

        # === Additional Cross-Category Classics ===
        {"title": "Talking to Strangers: What We Should Know about the People We Don't Know", "author": "Malcolm Gladwell", "isbn": "9780316478526", "publication_year": "2019", "category": "Social Intelligence"},
        {"title": "Blink: The Power of Thinking Without Thinking", "author": "Malcolm Gladwell", "isbn": "9780316010665", "publication_year": "2005", "category": "Self-Awareness"},
        {"title": "The Sociopath Next Door", "author": "Martha Stout", "isbn": "9780767915823", "publication_year": "2005", "category": "Social Intelligence"},
        {"title": "Give and Take: Why Helping Others Drives Our Success", "author": "Adam Grant", "isbn": "9780143124986", "publication_year": "2013", "category": "Relationships"},
        {"title": "Think Again: The Power of Knowing What You Don't Know", "author": "Adam Grant", "isbn": "9781984878106", "publication_year": "2021", "category": "Self-Awareness"},
        {"title": "Stumbling on Happiness", "author": "Daniel Gilbert", "isbn": "9781400077427", "publication_year": "2006", "category": "Self-Awareness"},
        {"title": "The Social Animal: The Hidden Sources of Love, Character, and Achievement", "author": "David Brooks", "isbn": "9780812979374", "publication_year": "2011", "category": "Social Intelligence"},
        {"title": "Outliers: The Story of Success", "author": "Malcolm Gladwell", "isbn": "9780316017930", "publication_year": "2008", "category": "Self-Management"},
        {"title": "Range: Why Generalists Triumph in a Specialized World", "author": "David Epstein", "isbn": "9780735214484", "publication_year": "2019", "category": "Self-Awareness"},
        {"title": "Originals: How Non-Conformists Move the World", "author": "Adam Grant", "isbn": "9780525429562", "publication_year": "2016", "category": "Leadership"},
        {"title": "Hidden Potential: The Science of Achieving Greater Things", "author": "Adam Grant", "isbn": "9780593653142", "publication_year": "2023", "category": "Self-Management"},
        {"title": "The Culture Code: The Secrets of Highly Successful Groups", "author": "Daniel Coyle", "isbn": "9780804176989", "publication_year": "2018", "category": "Leadership"},
        {"title": "An Everyone Culture: Becoming a Deliberately Developmental Organization", "author": "Robert Kegan", "isbn": "9781625278623", "publication_year": "2016", "category": "Leadership"},
        {"title": "Emotional Blackmail: When the People in Your Life Use Fear, Obligation, and Guilt to Manipulate You", "author": "Susan Forward", "isbn": "9780060928971", "publication_year": "1997", "category": "Conflict Resolution"},
        {"title": "Games People Play: The Psychology of Human Relationships", "author": "Eric Berne", "isbn": "9780345410030", "publication_year": "1964", "category": "Relationships"},
        {"title": "How to Be an Adult in Relationships: The Five Keys to Mindful Loving", "author": "David Richo", "isbn": "9781570628122", "publication_year": "2002", "category": "Relationships"},
        {"title": "The Dance of Anger: A Woman's Guide to Changing the Patterns of Intimate Relationships", "author": "Harriet Lerner", "isbn": "9780062319043", "publication_year": "2014", "category": "Conflict Resolution"},
        {"title": "Surrounded by Idiots: The Four Types of Human Behavior", "author": "Thomas Erikson", "isbn": "9781250179944", "publication_year": "2019", "category": "Social Intelligence"},
        {"title": "The Art of Gathering: How We Meet and Why It Matters", "author": "Priya Parker", "isbn": "9781594634932", "publication_year": "2018", "category": "Social Intelligence"},
        {"title": "Presence: Bringing Your Boldest Self to Your Biggest Challenges", "author": "Amy Cuddy", "isbn": "9780316256575", "publication_year": "2015", "category": "Self-Awareness"},
        {"title": "Reclaiming Conversation: The Power of Talk in a Digital Age", "author": "Sherry Turkle", "isbn": "9780143109792", "publication_year": "2015", "category": "Communication"},
        {"title": "Conversational Intelligence: How Great Leaders Build Trust and Get Extraordinary Results", "author": "Judith E. Glaser", "isbn": "9781937134679", "publication_year": "2013", "category": "Communication"},
        {"title": "On Dialogue", "author": "David Bohm", "isbn": "9780415336413", "publication_year": "2004", "category": "Communication"},
        {"title": "Why Won't You Apologize?: Healing Big Betrayals and Everyday Hurts", "author": "Harriet Lerner", "isbn": "9781501129605", "publication_year": "2017", "category": "Conflict Resolution"},
        {"title": "Who Moved My Cheese?", "author": "Spencer Johnson", "isbn": "9780399144462", "publication_year": "1998", "category": "Self-Management"},
        {"title": "Predictably Irrational: The Hidden Forces That Shape Our Decisions", "author": "Dan Ariely", "isbn": "9780061353246", "publication_year": "2008", "category": "Self-Awareness"},
    ]

    for b in books:
        b["source"] = "curated_seed"

    return books
