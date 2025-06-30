---
article: 
    publishedTime: "2025-06-30T02:07:41Z"
    modifiedTime: "2025-06-30T02:07:41Z"
    authors: ["Joo Gyeong Kim", "Kaylie Marie Nakaya", "Saan Lily Popović", "Violet Monserate"]
    section: Personal Projects
    tags: ["figma", "HCI", "UX"]
layout: '@components/MarkdownProjectLayout.astro'
title: ChefMate
description: Group project for CSE 440 Human-Computer Interaction course, where we researched and developed a novel commercial product
seoDescription: Group project for CSE 440 Human-Computer Interaction course, where we researched and developed a novel commercial product
image:
    src: "@assets/chefmate/chefmate.png"
    alt: "A mom, dad, and child in front of a refridgerator with a hat on beige background with ChefMate at the bottom."
startDate: '2025-04'
finishDate: '2025-06'
icons: ["figma"]
---

![A mom, dad, and child in front of a refridgerator with a hat on beige background with ChefMate at the bottom](@assets/chefmate/chefmate.png) 

---

## Problem and Solution Overview

Every family needs to eat; however, time is not on the side of a busy parent. For many families — especially those with young children — meal preparation can feel more like a stressful chore than an enjoyable bonding experience. Parents often juggle their busy schedules with budgeting weekly grocery trips and planning meals, leaving them with little time to involve their children in cooking.

Modern support includes meal or grocery delivery services, cooking accounts and recipes spread across the internet, and the support of family and friends. However, this support is not always enough to overcome the challenges that keep families from having healthy, regular meals.

To consolidate and improve these solutions, we have created ChefMate. ChefMate is more than just a refrigerator. Assisting the user to develop cost-effective grocery lists based on weekly grocery prices, recommending meals based on individual time constraints, preferences, and accessible ingredients, ChefMate utilizes artificial intelligence to tailor these recommendations to the user. Additionally, ChefMate includes a “child mode” for parents of young children to cook with their children. This will aid parents when involving their children in dinner preparation and cooking by simplifying recipes and providing small tasks for young children.

## Design Research Goals, Stakeholders, and Participants

Our goal with ChefMate is to help families have regular meals together. Through initial research and discussion, we concluded that there is a particular need within families with young children, 2–5 years old, who could use a helping hand with cooking. We contacted families that have children of various ages, eating traditions, and cultures to understand and learn about their perspectives. We initially sent each participant a brief survey to gather data from parents in order to minimize completion time. We hoped to gather data without taking away time from their already busy schedules. The survey included an option to follow up in a more detailed diary study. The diary study consisted of a short write up about an example of meal preparation for parents with more time. This helped us to collect more longitudinal data and specific details about recent mealtimes.

## Design Research Results and Themes

We surveyed 27 parents with zero to six children, ranging from nine months to 20 years old. Most participants had 1, 2, or 3 children with an average age of 8; however, one participant had zero children and one had six. We received various responses from the families, some eating dinner together regularly, and some eating separately. In some families, only adults cook in some families, while in others, children are involved in meal preparation. We received five diary study entries from our pool of participants.

According to the survey responses, the most prominent challenge our participants face is time, both grocery shopping and cooking, followed by budget and cooking skills.

![Pie chart with title "What is the hardest element of cooking for your family?", with 55.6% saying "time"](@assets/chefmate/hardest-element.webp)
*Fig 1: A vast majority of folks still believe time is the biggest barrier for cooking*

Many participants mentioned that while grocery shopping can be an opportunity for family bonding, it often takes a lot of time to come up with a grocery list meeting budget requirements and find the time to cook on the day they grocery shop.

![Pie chart with title "What is the hardest part of shopping?", with 51.9% saying "time", 18.5% saying budget](@assets/chefmate/hardest-part.webp)
*Fig 2: Shopping follows a similar pattern to cooking, where parents are under a time crunch*

Many participants struggle to find time to cook meals for their families, and they particularly find it difficult to cook something that meets every member’s dietary preferences and restrictions. The food restrictions our participants listed included allergies, eating disorders, diabetes, kosher, pescatarian, gluten-free, and keto diets. Some food preferences our participants listed included foods they disliked, some children being very picky eaters, and health goals like reducing cholesterol. One participant said, “The adult with high cholesterol cannot eat cheese, egg, or red meat, while the one with food aversions will only eat certain foods such as pasta, rice, red meat, and cheese. Not much overlap between those diets.” While another participant also struggles with motivation due to this barrier, telling us that the most complicated things are “time and energy, between long workdays and afternoon/evening extracurriculars, it’s often difficult to carve out the time to cook, and also feels not worth it if not everyone will be home, or isn’t hungry (our kids are also independent enough that they often snack or get food outside the home on their own); it’s also demotivating to feel like someone will complain about some element of any meal we try.”

To combat this challenge, our participants have tried cutting fruits and vegetables into shapes to increase their appeal and using mealtimes like dinner as a bonding activity for the family. However, both of these modifications increase the problem of limited time. Parents feel like they are stretched too thin between planning grocery trips, making lists based on ingredients in the fridge, and cooking meals.

## Task development

While trying to figure out how our solution would shape up, we developed user tasks to see how well a potential solution holds up. Below is one of those tasks, in which we explore how a parent develops/finds recipes that accommodate the dietary needs of all family members while maintaining a solid budget.

![](@assets/chefmate/task-1.webp)

![](@assets/chefmate/task-2.webp)
*Fig 3 & 4: A storyboard demonstrating how the fridge will scan your fridge and offer recipes*

## Our Solution: ChefMate!

To improve upon existing solutions, we have designed ChefMate. ChefMate is so much more than just a refrigerator. Assisting users in developing cost-effective grocery lists based on weekly grocery prices and recommending meals tailored to a family’s time constraints, dietary preferences, and available ingredients, ChefMate is a smart refrigerator that utilizes artificial intelligence to provide personalized recommendations.

Additionally, ChefMate includes a “child mode” setting for parents of young children to help them to easily include their children with cooking. A suite of sensors and cameras within the refrigerator enables the ChefMate to precisely determine which ingredients are available. With the addition of spotlights, ChefMate directs any user toward the right ingredients for their chosen recipe and which are going bad. The child-mode will use this feature and others to aid parents when involving their children in dinner preparation and cooking by simplifying recipes and providing small tasks for young children. Not only will this help parents teach their children cooking skills, but it will also help build connections with them. ChefMate is not only here to make cooking easier, but also to create a community in the kitchen and provide every member of the household with the opportunity to express their creativity through cuisine.

![Shows child scrolling on screen, with an example UI on the right hand side](@assets/chefmate/sketch.webp)
*Fig 5: Initial sketch of ChefMate*

## Paper Prototype & Usability Tests

After creating our initial design and sketches, we proceeded to create a detailed paper prototype of the different pages on our ChefMate refrigerator’s screen. These interactive paper prototypes were made to test our design and improve features before building digital mockups. These paper prototypes were not static and were designed with different workflows in mind. To allow users to interact with the prototypes during testing.

During user testing, the first task was from the perspective of a parent who is preparing the kitchen for the week. There is food in the fridge (including ingredients that had gone bad), and we asked the parent to (a) generate a list of recipes to make for the week and (b) generate the groceries and shopping list necessary for the week! They used the screen on the refrigerator to accomplish these tasks. The second task during user testing was from the perspective of a child in the kitchen. We asked for the parents to bring their child or imagine they were cooking with their child. We told the parents to select a recipe to cook together and turn on child-mode. We told the children to imagine their parents had asked them to help out in the kitchen, and their task is to use the refrigerator and follow its directions to help their parents cook the recipe.

![Paper prototype to facilitate usability tests, made with regular office supplies, showing home screen, pick your store, and your choices](@assets/chefmate/paper-prototype.png)
*Fig 6: Our initial paper prototype made with office supplies*

![A flowchart showing the different screens users click on to create grocery lists](@assets/chefmate/generate-recipes.webp)
*Fig 7: A simple workflow through the paper prototype, generating a whole shopping list for parents*

![Another example workflow through the paper prototype from the perspective of a child, as they help their parent cook](@assets/chefmate/child-mode.webp)
*Fig 8: Another example workflow from the perspective of a child, as they help their parent cook*

Through testing our initial prototype with other designers in the course, we found two major issues: 
1. We were missing some buttons that would improve the user’s navigation experience (such as the back button and home button), reducing the safety of the system, and 
2. Putting the child mode button too low down may cause problems if the children can toggle it themselves. Considering the feedback we collected during this user testing, we revised our paper prototype before testing it with our target users.

Notable features that were initially included in our prototype include the ability to set up a profile with meal preferences and portion sizes, scroll through and select different fields (recipes, ingredients, and portion sizes), a home button in the bottom right, and a labeled homescreen. As we continued to refine the prototype, we added, removed, and modified features to ensure users had seamless experience with ChefMate.

The second round of usability tests was conducted with multiple mothers, a father, and two children pretending to cook with their parents, which allowed us to see how our real user base would interact with ChefMate. During the process, we discovered that it was critical to include a guide or help page detailing each feature, as some users were confused and missed some of ChefMate’s features entirely. The other most significant change we had to make to our prototype was to add a calendar feature. Some usability test participants were looking for a feature that would allow them to plan their meals for the week. They stated they wished for more detailed planning rather than just our initial functionality of saving recipes. These participants hoped to be able to see which ingredients they need to save and which they need for each day.

![A spread of different paper screens demonstrating the final paper prototype of the project](@assets/chefmate/paper-final.png)
*Fig 9: A complete layout of the final paper prototype after user testing*

This essential feedback was directly taken into consideration when revising our design and creating the final digital mockup.

## Digital Mockup

After conducting usability tests and reviewing the participants’ feedback, we incorporated their input into our paper prototypes to enhance our design. Once we refined and finalized the paper prototypes, we created a digital version of the prototypes to show ChefMate’s screen.

![A digital wireframe on Figma, with orange and beige colors](@assets/chefmate/figma.png)
*Fig 10: A digital wireframe on Figma, which can be [accessed here](https://www.figma.com/design/JQej8UoE18IzCUn1cXzr7t/CSE440---ChefMate-Digital-Prototype?node-id=0-1&p=f&t=0ppQlteyP0yMLUEL-0)*

![A flowchart showing the different screens users click on to create grocery lists](@assets/chefmate/generate-recipes-digital.png)
*Fig 11: The same task of generating a whole shopping list, but through our digital prototype*

![Another example workflow through the digital prototype from the perspective of a child, as they help their parent cook](@assets/chefmate/child-mode-digital.png)
*Fig 12: The child mode recipe task, as viewed from our digital prototype*

## Summary

We all need to eat balanced meals to stay healthy, but meal planning and cooking can be challenging, especially for those who are busy, including parents of young children. ChefMate supports these individuals who are seeking an efficient way to tackle this problem. However, we also hope that the new ease of cooking with ChefMate will help users view cooking as a form of creativity and a bonding opportunity by removing the stress from the question of “what’s for dinner?” By providing meal-planning, grocery shopping, and child-mode features, we believe this innovative solution will encourage users to continue exploring and learning cooking skills, enabling them to spend more time connecting with others inside and outside of the kitchen.