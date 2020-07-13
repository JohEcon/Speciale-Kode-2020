import numpy

#We define the probability of death at a given age:
def prop_death(age):
    x = 0.0005 + 10 ** (-4.2 + 0.038 * age)
    y = (1+x)**(1/Settings.periods_in_year)-1
    return y

#we define the household utility function

"""def household_utility(household, house):
    annuity = Bank.get_annuity(Simulation.Banks.get_random_agent(), house.price - household.equity, Settings.loan_lenght, Settings.periods_in_year)
    spending = household.income - annuity
    quality = house.quality
    a = household.utility_alpha
    cd_utility = (spending ** a) * (quality ** (1 - a))
    return cd_utility"""

#we define a method to pay taxes on income
def pay_income_taxes(income):
    after_tax_income = 0
    arb_bidrag = income * Settings.arbejdsmarkedsbidrag
    bundskat = 0
    topskat = 0

    if income >= Settings.bundfradrag/Settings.periods_in_year and income >0:
        bundskat = (income-Settings.bundfradrag/Settings.periods_in_year) * Settings.bundskat

    if income > Settings.topskat_limit/Settings.periods_in_year:
        topskat = (income - Settings.topskat_limit/Settings.periods_in_year) * Settings.topskat

    if income >0:
        after_tax_income = income - arb_bidrag - bundskat - topskat
        skattetryk = (1 - after_tax_income / income)

    if (1 - skattetryk) < (1 - (Settings.skatteloft + Settings.arbejdsmarkedsbidrag)):
        after_tax_income = income * (1 - (Settings.skatteloft + Settings.arbejdsmarkedsbidrag))

    return after_tax_income


def sort_data (x,y):
    xx, yy = (list(t) for t in zip(*sorted(zip(x, y))))
    return xx, yy

def local_mean(x,y, n=10):
    """Calculating local means. Poor man's loess. Fine and quick if many data points.
    The algorithm works like this:
          1) x and y are sorted according to x,
          2) the data is split in n equally sized parts, and
          3) means are calculated for both x and y in each part.

    Arguments:
        x (list) -- The x data
        y {list} -- The y data

    Keyword Arguments:
        n {int} -- The number of parts (default: {10})

    Returns:
        {list, list} -- n mean values of x and y
    """

    xx, yy = (list(t) for t in zip(*sorted(zip(x, y)))) # sort x and y after x

    if n <= len(x):
        m = int(len(x)/n) # Number of data points in each group
    else:
        m = 1
    k = len(x) % n
    if k != 0 and len(x)/n > 1:
        p = 1
    else:
        p = 0

    x_o, y_o = [], []
    x_sum, y_sum, v = 0, 0, 0
    j = 0

    if len(x) > 0:
        for i in range(len(x)):

            if v < (m + p) and j < n:
                v += 1
                x_sum += xx[i]
                y_sum += yy[i]

            if v == (m + p) and j < n:
                x_o.append(x_sum/(m + p))
                y_o.append(y_sum/(m + p))
                x_sum, y_sum, v = 0, 0, 0
                j += 1

            if i == k*(m + 1) -1:
                p = 0

        return x_o, y_o
    else:
        return None


def local_mean_get_value(x, x_lm, y_lm):

    if x < x_lm[0]:
        return y_lm[0] + (x - x_lm[0]) * (y_lm[1] - y_lm[0]) / (x_lm[1] - x_lm[0])

    if x > x_lm[-1]:
        return y_lm[-1] + (x - x_lm[-1]) * (y_lm[-1] - y_lm[-2]) / (x_lm[-1] - x_lm[-2])

    else:
        for i in range(len(x_lm)):
            if x >= x_lm[i]:
                    return y_lm[i] + (x - x_lm[i]) * (y_lm[i + 1] - y_lm[i]) / (x_lm[i + 1] - x_lm[i])
                    break

class Settings: pass
#Number of agents and periods settings
Settings.number_of_agents = 500
Settings.number_of_banks = 1
Settings.number_of_houses = 500
Settings.number_of_periods = 1000
Settings.periods_in_year = 12

#House selling and buying settings
Settings.max_houses_checked = 30
Settings.price_adjustment_frequency = 2
Settings.price_adjustment = -0.02
Settings.houses_surveyed = 4
Settings.price_premium = 1.05
Settings.periods_between_price_assessment = 12
Settings.utility_ratio_minimum = 0.1

#tax settings
Settings.bundfradrag = 46500
Settings.topskat_limit = 531000 * 1.08
Settings.arbejdsmarkedsbidrag = 0.08
Settings.bundskat = 0.26 + 0.0075 + 0.1211
Settings.topskat = 0.15
Settings.skatteloft = 0.5206
Settings.interest_tax = 0.25

#income and age settings
Settings.starting_income = 10000
Settings.su_income = 6200
Settings.kh_income = 11500
Settings.pension_share = 0.8
Settings.starting_age = 20
Settings.retire_age = 67
Settings.max_age = 109
Settings.minimum_disposable = 2000
Settings.minimum_disposable_ratio = 0.1

#Bank and loan settings
Settings.starting_interest = 0.01
Settings.piti_multiplier = 0.28
Settings.interest = 0.04
Settings.loan_length = 30
Settings.max_low_income_count = 5

#other settings
Settings.utility_alpha = 0.5
Settings.random_seed = 1 #If equal to 0, seed is random
Settings.out_file = "Statistics.py"
Settings.graphics_show = False
Settings.graphics_periods_per_pic = 12
Settings.ratio_print = 0.02
Settings.number_of_batches = 5
Settings.rent_quality = 0.05
Settings.rent_annuity = 2500


# We create an event class
class Event: pass
Event.start = 1  # The model starts
Event.stop = 2  # The model stops
Event.period_start = 3 #
Event.update = 4 # Agent behavior
Event.period_end = 5 #consolidation of what happened last period
Event.update_year = 6 #Agent behavior which only happends once a year

class Communication: pass
Communication.buy_house = 1
Communication.sell_house = 2

