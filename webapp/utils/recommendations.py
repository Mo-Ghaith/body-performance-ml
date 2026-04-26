"""
utils/recommendations.py — Generate personalized diet and exercise plans based on predicted class.
"""


def recipe_link(text, url):
    return f'<a href="{url}" target="_blank" style="color: #3B82F6; text-decoration: none; border-bottom: 1px dotted rgba(59, 130, 246, 0.5);">{text}</a>'

def get_diet_plan(class_label, bmi, body_fat, gender):
    """Generate personalized diet recommendations."""
    plans = {
        'A': {
            'title': '🥗 Elite Maintenance Plan',
            'calories': '2,200 – 2,800 kcal/day' if gender == 'M' else '1,800 – 2,200 kcal/day',
            'protein': '1.6–2.0g per kg body weight',
            'carbs': '45–55% of total calories',
            'fats': '25–30% of total calories',
            'hydration': '3.5–4.0 liters/day',
            'meals': [
                ('🌅 Breakfast', f"{recipe_link('Oatmeal with berries', 'https://www.eatingwell.com/recipe/261907/oatmeal-with-fruit-nuts/')}, eggs, {recipe_link('avocado toast', 'https://www.wellplated.com/avocado-toast/')}, green smoothie"),
                ('🥗 Lunch', f"{recipe_link('Grilled chicken salad with quinoa', 'https://www.skinnytaste.com/grilled-chicken-quinoa-salad/')}, mixed greens, olive oil dressing"),
                ('🍎 Snack', f"Greek yogurt with almonds, {recipe_link('protein shake', 'https://www.bodybuilding.com/recipes')} post-workout"),
                ('🥘 Dinner', f"{recipe_link('Salmon with sweet potato', 'https://www.bbcgoodfood.com/recipes/salmon-sweet-potato-mash')} and steamed broccoli"),
                ('🌙 Evening', 'Casein protein, herbal tea, small handful of walnuts'),
            ],
            'tips': [
                'Focus on anti-inflammatory foods to maintain peak performance',
                'Cycle carbs around training days for optimal energy',
                'Prioritize post-workout nutrition within 30 minutes',
                'Include omega-3 rich fish 3-4 times per week',
            ]
        },
        'B': {
            'title': '🍽️ Performance Growth Plan',
            'calories': '2,400 – 3,000 kcal/day' if gender == 'M' else '1,900 – 2,400 kcal/day',
            'protein': '1.8–2.2g per kg body weight',
            'carbs': '45–50% of total calories',
            'fats': '25–30% of total calories',
            'hydration': '3.0–3.5 liters/day',
            'meals': [
                ('🌅 Breakfast', f"{recipe_link('Whole grain pancakes with banana', 'https://www.eatingwell.com/recipe/269866/three-ingredient-banana-pancakes/')}, scrambled eggs, fresh juice"),
                ('🥗 Lunch', f"{recipe_link('Turkey wrap with veggies', 'https://www.skinnytaste.com/turkey-club-wrap/')}, hummus, side of lentil soup"),
                ('🍎 Snack', f"{recipe_link('Healthy trail mix', 'https://www.eatingwell.com/recipe/269145/healthy-trail-mix/')}, apple with peanut butter"),
                ('🥘 Dinner', f"{recipe_link('Lean beef stir-fry', 'https://www.bbcgoodfood.com/recipes/healthy-beef-broccoli-stir-fry')} with brown rice, mixed vegetables"),
                ('🌙 Evening', 'Cottage cheese with chia seeds'),
            ],
            'tips': [
                'Slightly increase protein to build lean muscle mass',
                'Time carbs around workouts for better performance',
                'Add creatine monohydrate (5g/day) for strength gains',
                'Eat more leafy greens for micronutrient support',
            ]
        },
        'C': {
            'title': '🥑 Balanced Improvement Plan',
            'calories': '2,000 – 2,500 kcal/day' if gender == 'M' else '1,600 – 2,000 kcal/day',
            'protein': '1.4–1.8g per kg body weight',
            'carbs': '40–50% of total calories',
            'fats': '25–35% of total calories',
            'hydration': '2.5–3.0 liters/day',
            'meals': [
                ('🌅 Breakfast', f"{recipe_link('Greek yogurt parfait', 'https://www.skinnytaste.com/yogurt-and-fruit-parfaits/')} with granola and mixed berries"),
                ('🥗 Lunch', f"Grilled chicken with brown rice and {recipe_link('roasted vegetables', 'https://www.eatingwell.com/recipe/252684/roasted-vegetables/')}"),
                ('🍎 Snack', 'Banana, handful of almonds, protein bar'),
                ('🥘 Dinner', f"{recipe_link('Baked fish with quinoa', 'https://www.mindbodygreen.com/0-24424/the-only-baked-fish-recipe-youll-ever-need.html')} and steamed asparagus"),
                ('🌙 Evening', 'Herbal tea, small bowl of mixed nuts'),
            ],
            'tips': [
                'Reduce processed food intake by 50%',
                'Start tracking meals to build awareness',
                'Increase vegetable intake to 5+ servings/day',
                'Replace sugary drinks with water or green tea',
            ]
        },
        'D': {
            'title': '🌿 Foundation Building Plan',
            'calories': '1,800 – 2,200 kcal/day' if gender == 'M' else '1,400 – 1,800 kcal/day',
            'protein': '1.2–1.6g per kg body weight',
            'carbs': '40–45% of total calories',
            'fats': '25–35% of total calories',
            'hydration': '2.5–3.0 liters/day',
            'meals': [
                ('🌅 Breakfast', f"Whole wheat toast with eggs, orange juice, {recipe_link('healthy banana smoothie', 'https://www.eatingwell.com/recipe/252187/banana-smoothie/')}"),
                ('🥗 Lunch', f"{recipe_link('Brown rice bowl with chicken', 'https://www.bbcgoodfood.com/recipes/chicken-brown-rice-bowl')} and mixed greens"),
                ('🍎 Snack', 'Apple slices with almond butter, low-fat yogurt'),
                ('🥘 Dinner', f"{recipe_link('Lean turkey sweet potato skillet', 'https://www.skinnytaste.com/turkey-sweet-potato-skillet/')} with green beans"),
                ('🌙 Evening', 'Warm milk, small serving of fruit'),
            ],
            'tips': [
                'Start with small sustainable changes, not drastic diets',
                'Eliminate one unhealthy habit per week',
                'Drink a glass of water before every meal',
                'Cook at home at least 5 days a week',
            ]
        },
    }

    plan = plans.get(class_label, plans['C'])

    # Add BMI-specific advice
    if bmi > 30:
        plan['tips'].append('⚠️ Your BMI indicates obesity — consider a caloric deficit of 300-500 kcal')
    elif bmi > 25:
        plan['tips'].append('📊 BMI is in the overweight range — focus on portion control and activity')
    elif bmi < 18.5:
        plan['tips'].append('📊 BMI is underweight — increase caloric intake with nutrient-dense foods')

    return plan


def get_exercise_plan(class_label, age, grip_force, flexibility, sit_ups, broad_jump):
    """Generate personalized exercise recommendations."""
    plans = {
        'A': {
            'title': '🏆 Elite Training Program',
            'weekly_sessions': '5-6 days/week',
            'intensity': 'High',
            'categories': [
                {
                    'name': '💪 Strength',
                    'icon': '🏋️',
                    'exercises': [
                        'Barbell squats (4×6-8)',
                        'Deadlifts (4×5-6)',
                        'Bench press (4×6-8)',
                        'Pull-ups weighted (4×6-8)',
                        'Olympic lifts (power clean, snatch)',
                    ]
                },
                {
                    'name': '🤸 Flexibility',
                    'icon': '🧘',
                    'exercises': [
                        'Dynamic stretching routine (15 min)',
                        'Yoga flow (30 min, 2×/week)',
                        'Foam rolling recovery',
                        'PNF stretching for tight areas',
                    ]
                },
                {
                    'name': '❤️ Cardio & Endurance',
                    'icon': '🏃',
                    'exercises': [
                        'HIIT intervals (20 min, 2×/week)',
                        'Zone 2 cardio (40-60 min, 2×/week)',
                        'Sprint training (1×/week)',
                        'Sport-specific conditioning',
                    ]
                },
            ],
            'recovery': 'Active recovery days with light stretching, swimming, or walking',
        },
        'B': {
            'title': '💪 Growth Training Program',
            'weekly_sessions': '4-5 days/week',
            'intensity': 'Moderate-High',
            'categories': [
                {
                    'name': '💪 Strength',
                    'icon': '🏋️',
                    'exercises': [
                        'Squats (3×8-10)',
                        'Romanian deadlifts (3×8-10)',
                        'Dumbbell press (3×8-10)',
                        'Lat pulldowns (3×10-12)',
                        'Core circuit (planks, leg raises)',
                    ]
                },
                {
                    'name': '🤸 Flexibility',
                    'icon': '🧘',
                    'exercises': [
                        'Full-body stretching (10-15 min daily)',
                        'Yoga or mobility class (1×/week)',
                        'Hip flexor and hamstring focus',
                    ]
                },
                {
                    'name': '❤️ Cardio & Endurance',
                    'icon': '🏃',
                    'exercises': [
                        'Moderate jog (30 min, 2×/week)',
                        'HIIT circuit (15-20 min, 1×/week)',
                        'Cycling or swimming (1×/week)',
                    ]
                },
            ],
            'recovery': '1-2 rest days with light mobility work',
        },
        'C': {
            'title': '🎯 Balanced Fitness Program',
            'weekly_sessions': '3-4 days/week',
            'intensity': 'Moderate',
            'categories': [
                {
                    'name': '💪 Strength',
                    'icon': '🏋️',
                    'exercises': [
                        'Bodyweight squats (3×12-15)',
                        'Push-ups (3×10-15)',
                        'Dumbbell rows (3×10-12)',
                        'Lunges (3×10 each leg)',
                        'Plank holds (3×30-45 sec)',
                    ]
                },
                {
                    'name': '🤸 Flexibility',
                    'icon': '🧘',
                    'exercises': [
                        'Basic stretching routine (10 min daily)',
                        'Toe touches and hamstring stretches',
                        'Cat-cow and child\'s pose',
                    ]
                },
                {
                    'name': '❤️ Cardio & Endurance',
                    'icon': '🏃',
                    'exercises': [
                        'Brisk walking (30 min, 3×/week)',
                        'Light jogging (20 min, 1-2×/week)',
                        'Jump rope (10 min sessions)',
                    ]
                },
            ],
            'recovery': '2-3 rest days, focus on sleep quality (7-8 hours)',
        },
        'D': {
            'title': '🌱 Foundation Building Program',
            'weekly_sessions': '3 days/week',
            'intensity': 'Low-Moderate',
            'categories': [
                {
                    'name': '💪 Strength',
                    'icon': '🏋️',
                    'exercises': [
                        'Wall push-ups (3×10)',
                        'Chair squats (3×10)',
                        'Resistance band pulls (3×12)',
                        'Dead bug exercise (3×8 each)',
                        'Glute bridges (3×12)',
                    ]
                },
                {
                    'name': '🤸 Flexibility',
                    'icon': '🧘',
                    'exercises': [
                        'Gentle morning stretches (5-10 min)',
                        'Seated hamstring stretches',
                        'Shoulder and neck rolls',
                        'Gentle yoga (beginner class)',
                    ]
                },
                {
                    'name': '❤️ Cardio & Endurance',
                    'icon': '🏃',
                    'exercises': [
                        'Walking (20-30 min daily)',
                        'Stair climbing (start with 2 flights)',
                        'Light cycling (15-20 min)',
                    ]
                },
            ],
            'recovery': 'Rest between sessions, prioritize 8+ hours sleep',
        },
    }

    plan = plans.get(class_label, plans['C'])

    # Age-specific adjustments
    if age > 50:
        plan['categories'][0]['exercises'].append('⚠️ Focus on controlled movements, avoid heavy maximal lifts')
        plan['categories'][1]['exercises'].append('🔑 Daily mobility work is essential at your age')

    # Weakness-specific additions
    if grip_force < 30:
        plan['categories'][0]['exercises'].append('🎯 Add: Farmer\'s walks and grip trainers (daily)')
    if flexibility < 5:
        plan['categories'][1]['exercises'].append('🎯 Priority: Dedicated flexibility sessions (15 min, 4×/week)')
    if sit_ups < 20:
        plan['categories'][0]['exercises'].append('🎯 Add: Core progression (dead bugs → crunches → sit-ups)')
    if broad_jump < 150:
        plan['categories'][0]['exercises'].append('🎯 Add: Box jumps and explosive leg training')

    return plan


def get_motivational_message(class_label):
    """Return motivational message with emojis based on class."""
    messages = {
        'A': [
            "🏆 You're a fitness machine! Keep pushing boundaries!",
            "⭐ Elite-level performance — you inspire others!",
            "🔥 Champion status! Maintain your edge with smart recovery.",
        ],
        'B': [
            "💪 Strong showing! You're close to the top tier!",
            "🚀 Just a few tweaks away from excellence!",
            "⚡ Great foundation — let's build something incredible!",
        ],
        'C': [
            "🎯 You're at the perfect starting point for growth!",
            "📈 Consistency is your superpower — keep going!",
            "🌟 Every champion started where you are now!",
        ],
        'D': [
            "🌱 Your fitness journey begins today — embrace it!",
            "💡 Small steps daily lead to massive transformations!",
            "🦋 Every expert was once a beginner. You've got this!",
        ],
    }
    import random
    return random.choice(messages.get(class_label, messages['C']))
