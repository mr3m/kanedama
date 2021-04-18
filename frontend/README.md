# :crystal_ball: Mansa Frontend Developer Coding Test

Welcome to Mansa's Frontend technical test! 

Be sure to read **all** of this document carefully, and follow the guidelines within.

## :godmode: About Mansa

At Mansa, we are on a mission to make freelancers workers spend less time on bureaucracies and more time using their money consciously, giving them access to loans with lower interest rates and longer term. To achieve this, we are developing a platform that involves the entire product chain and we aim to become leaders in credit services in Europe.

To face this challenge, we need people who believe in the impact of our business on one country's economy. More than that, we want to work with people who are not content with the obvious, who participate, without being afraid of making mistakes and learning, and who inspire others, with ideas to simplify people's routine.

Good luck! :boom:

## Context

The goal of this test is to create a dashboard-like user interface, where we can find:

- User's personal information
  - First & Last name
- User's business information
  - SIRET number
  - Creation date
  - Address (example: 10 Rue Gabriel Peri 92120, Montrouge)
- User's financial information
  - Account type {TRANSACTION / SAVINGS}
  - Current balance

In order not to influcence your design choices, we will not provide you with a wireframe to follow or a screenshot of our current dashboard.

The view should only be for **one** user.

You will need to leverage an open API for business data to fill in the details and functionality as described below. 

## Requirements

For simplicity reasons and in order for the test not to be too long to complete, you are only required to develop the page to fit the viewport of the device of your choice : either **mobile** or **desktop**.

### Tech stack

At Mansa, we're big fans of React. Our stack consists of TypeScript, React, [Next.js](https://nextjs.org/), CSS-in-JS with [styled-component](https://styled-components.com/), Flex & Grid, and we test with Jest and Cypress. 

The bare minimum is to complete the task with React. If you're comfortable with it, we encourage you to complete the test in the stack described above.

You're also free to use a component library to get you started and any other package that you might think is necessary.

Static type checking is a great way to introduce additional level of safety into your code and we welcome solutions written in TypeScript, but JavaScript is good too.

The use of component libraries, like Material UI, might make this easier and quicker for you but keep in mind that using it means we'll have less code to assess your knowledge and Frontend skills. Feel free to use a js chart library if you want too.

We expect you to test your code: the minimum requirement is unit tests, end to end tests are a big plus. From our experience Cypress.js works very well for React application testing, but you're free to pick your favourite.

Remarks:

- Use es6 or later, do not use es5
- Do **not** use jQuery
- Feel free to use vanilla css, CSS-in-JS, or utility-first libraries

### SIREN Api

For business information, we'll use the SIREN public API, you can find the documentation about it [here](https://entreprise.data.gouv.fr/api_doc/sirene).

We'll use the `unites_legales` object.

The URL is : `https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales/${SIREN_NUMBER}`

For example : <https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales/833079619>

You can choose any Siren you want for your test.

### Mansa API

For financial information, you'll use our custom API :

| Endpoint                                                            | Data                                                                                                                                                                                                                                                                                | Method |
| ------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------ |
| /accounts                                                           | Fetch all bank accounts from a _test user_.                                                                                                                                                                                                                                         | [GET]  |
| /accounts/:account*id/transactions?from=\_start_date*&to=_end_date_ | Fetch the specified _account_id_ transactions from the _start_date_ to the _end_date_. Date are ISO 8601 UTC, so for example `2018-08-13T03:24:00` It can't return more than **365 days** of transactions. If there are no date specified, the oldest transaction will be returned. | [GET]  |

Root endpoint is : <https://kata.getmansa.com/>

You can see our backend readme test if you want more information about this endpoint.

### :confetti_ball: Bonus

- Write **clear documentation** on how the app was designed and how to run the code
- Provide e2e tests
- Typescript
- Beautiful charts
- Write concise and clear commit messages
- Provide an online demo of the application, in a deployed environment
- User-friendly and clear UI
- Complete user information (Profil picture, phone number, etc ...) with another API like [randomuser](https://randomuser.me)
- Describe optimization opportunities and next steps as you conclude

### Design

The insights below are only here to show the information required and provide a baseline to your design choices and implementations. 

The 2 screenshots below do **not** represent our current dashboard nor the layout we necessarily expect: we provide no constraints regarding the UI and design in general, feel free to implement your own. 

![Design Draft1](./draft1.png)

![Design Draft1](./draft2.png)

## What We Care About

We're interested in your method and how you approach the problem just as much as we're interested in the end result.

Here's what you should strive for:

- Good use of current HTML, CSS, and JavaScript / TypeScript
- An keen eye for UX and user-friendly UI, without forgetting accessibility
- A consistent architecture, focused on the simplicity of the project (**keep it simple!**), a good programmer is a pragmatic programmer, no need to over-engineer things
- Extensible code
- Clean code using proper programming patterns and JavaScript best practices

## :gift: The Deliverable

- A link to an accessible private repository with your work in (Github can host personal private repositories for free), or a bundled/archived repository showing your commit history. Git example for sending us a standalone bundle:

        git bundle create <yourname>.bundle --all

- A README file explaining the decisions you've made solving this task including technology and library choices, and instructions required to run your solution and tests

## Q&A

> Where should I send back the result when I'm done?

Fork this repo and send us a pull request when you think you are done. There is no deadline for this task unless otherwise noted to you directly.
You can also directly send me your bundle at remy.tinco'@'getmansa'.com

> There's something on the task I don't understand

If you have a doubt and can't reach us to clarify it, make the assumption that feels more natural, document it and move on. We will evaluate based on that assumption.

For example, if you don't know which attribute you should list on the homepage choose some attributes and move on.

> Can I have some extra time to add more features ?

Adding extra features is great and we will look at them as well. But the best thing you can do if you have extra time is to complete as much as you can the features that are requested already. For example, try adding tests or more documentation, we will value that more than having a user management module.

> What if I have a question?

Just create a new issue in this repo and we will respond and get back to you quickly. You can also send me an email remy.tinco'@'getmansa'.com
Asking questions is good. We will not penalize you for asking questions.
