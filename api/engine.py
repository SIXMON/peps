from data.models import Problem, PracticeType, Weed, Pest
from data.models import Practice, Culture
from api.utils import AlpacaUtils
from api.models import ResponseItem


class Engine:

    form = None
    blacklisted_practices = []

    def __init__(self, answers, blacklisted_practices):
        self.form = AlpacaUtils(answers)
        self.blacklisted_practices = blacklisted_practices


    def calculate_results(self):
        """
        Returns an array of Response objects ordered by weight.
        """
        practices = Practice.objects.all()
        results = []

        for practice in practices:
            weight = self._calculate_weight(practice)
            results.append(ResponseItem(practice, weight))

        def _take_weight(elem):
            return elem.weight

        return sorted(results, key=_take_weight, reverse=True)

    def get_suggestions(self, results):
        """
        Given an array of Response objets it will return the suggestions
        to present to the user. It takes into consideration the difficulty
        of the practice and their score.
        """
        number_of_suggestions = 3
        minimum_weight = 0.5

        # We will only suggest practices above the minimum weight that have information on their difficulty.
        eligible_results = list(filter(lambda x: x.weight >= minimum_weight and x.practice.difficulty, results))
        eligible_results.sort(key=lambda x: x.practice.difficulty, reverse=True)

        # If we have less eligible results than number of suggestions needed, we just
        # return them
        if len(eligible_results) <= number_of_suggestions:
            return eligible_results

        # We will divide the list of difficulty-ordered items in chunks, and will
        # add the element of the highest weight of each chunk, as long as its practice
        # groups haven't been used before.
        chunk_size = len(eligible_results) // number_of_suggestions
        suggestions = []

        used_practice_groups = []
        for i in range(number_of_suggestions):

            # First we obtain the chunk in which we will select a practice.
            if i + 1 < number_of_suggestions:
                chunk = eligible_results[chunk_size * i : chunk_size * (i + 1)]
            else:
                chunk = eligible_results[chunk_size * i :]

            # We exclude all practices inside this chunk that are part of
            # groups that have already been used. For now I pass through the
            # airtable_json to avoid making a bunck of requests to the DB.
            eligible_chunk_practices = [x for x in chunk if x.practice.airtable_json['fields'].get('Famille', []) not in used_practice_groups]

            suggestion = max(eligible_chunk_practices, key=lambda x: x.weight)
            used_practice_groups.extend(suggestion.practice.airtable_json['fields'].get('Famille', []))
            suggestions.append(suggestion)


        return suggestions

    def _calculate_weight(self, practice):
        weight = 1
        form = self.form

        practice_added_cultures = [Culture(x) for x in (practice.added_cultures or [])]
        practice_target_cultures = [Culture(x) for x in (practice.target_cultures or [])]
        practice_problems_addressed = [Problem(x) for x in (practice.problems_addressed or [])]
        practice_weeds = [Weed(x) for x in (practice.weeds or [])]
        practice_pests = [Pest(x) for x in (practice.pests or [])]
        practice_types = [PracticeType(x) for x in (practice.types or [])]

        # If the practice is blacklisted we return 0
        # Eventually we should also decrease the score of similar practices
        if str(practice.id) in self.blacklisted_practices:
            return 0

        # If this practice applies to a culture that the user does not have, there
        # is no need to keep it. On the other hand, if the practice applies to a culture
        # the user has, we should bump it up a bit because it will be more relevant.
        target_culture_multiplier = 1.3
        if practice_target_cultures:
            if not form.cultures:
                return 0
            relevant_user_cultures = [x for x in form.cultures if x in practice_target_cultures]
            if not relevant_user_cultures:
                return 0
            else:
                weight *= target_culture_multiplier

        # If the practice adds a culture that the user already has,
        # we can return a score of 0
        if form.cultures and practice_added_cultures:
            redundant_cultures = [x for x in form.cultures if x in practice_added_cultures]
            if redundant_cultures:
                return 0

        # If the practice needs ground work / tillage and the
        # user can't carry it out, the score should be 0
        if practice.needs_tillage and form.tillage_feasibility is not None and not form.tillage_feasibility:
            return 0

        # If the practice is favorable or unfavorable to livestock
        # farms, it's score will change
        if form.livestock and practice.livestock_multiplier:
            weight *= float(practice.livestock_multiplier)

        # If the practice is favorable or unfavorable to direct sale
        # farms, it's score will change
        if form.direct_sale and practice.direct_sale_multiplier:
            weight *= float(practice.direct_sale_multiplier)

        # We check what kind of problem the user has to see if the practice
        # corresponds to it
        problem = form.problem
        correct_problem_multiplier = 1.5

        if problem and practice_problems_addressed and (problem in practice_problems_addressed):
            weight *= correct_problem_multiplier

        # Additionally, if the practice specifically targets one of the
        # pests or weeds the user is having problems with, we will bump it
        # even higher
        correct_target_multiplier = 1.2

        if problem == Problem.DESHERBAGE and form.weeds and practice_weeds:
            common_weeds = set(form.weeds).intersection(practice_weeds)
            if common_weeds:
                weight *= correct_target_multiplier

        if problem == Problem.RAVAGEURS and form.pests and practice_pests:
            common_pests = set(form.pests).intersection(practice_pests)
            if common_pests:
                weight *= correct_target_multiplier

        # We take a look at what kind of initiatives the user has already
        # tried. Given that we need more information for some, we will only
        # take into account the semis-direct and faux-semis.
        # In order to properly gauge couverts-vegetaux we would need to know
        # what kind of couvert was used.
        previosuly_tested_multiplier = 0.3

        if form.tested_practice_types and practice_types:

            if PracticeType.FAUX_SEMIS in form.tested_practice_types and PracticeType.FAUX_SEMIS in practice_types:
                weight *= previosuly_tested_multiplier

            elif PracticeType.SEMIS_DIRECT in form.tested_practice_types and PracticeType.SEMIS_DIRECT in practice_types:
                weight *= previosuly_tested_multiplier


        # We take a look at the advancement level to determine whether or not
        # this practice should be bumped up
        # TODO - How do we do it?
        advancement_level = form.advancement_level

        # Pratices have a multiplier related to the type of soil they are compatible
        # with. If the user specifies the type of soil we implement this multiplier
        user_soil_types = form.soil_types
        soil_type_multiplier = practice.get_user_soil_type_multiplier(user_soil_types)
        weight *= float(soil_type_multiplier)


        # We check the department. If the user department has a multiplier
        # in this practice we will use it.
        department_multiplier = practice.get_user_department_multiplier(form.department)
        weight *= float(department_multiplier)

        # We will multiply by the precision level to favor more
        # specific practices
        # TODO: What do I do with the precision ? I could combine it with weight and practice groups?
        # weight *= float(practice.precision)

        return weight
