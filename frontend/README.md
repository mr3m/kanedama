<p align="center"><a href="https://github.com/MansaGroup/kanedama" target="blank"><img src="../.github/assets/logo.png" width="80" alt="Mansa's Logo" /></a></p>
<h1 align="center">Mansa's Kanedama</h1>
<p align="center">Take host test to <b>join us</b> 💜</p>

## The Mission

Your mission, if you accept it, will be to create a dashboard-like user
interface, where we can find:

-   User's personal information
    -   First & Last name
-   User's business information
    -   SIRET number
    -   Creation date
    -   Address (example: 10 Rue Gabriel Peri 92120, Montrouge)
-   User's financial information
    -   Account type (TRANSACTION / SAVINGS)
    -   Current balance

### Design

In order not to influcence your design choices, we will not provide you
with a wireframe to follow or a screenshot of our current dashboard. But
with the following insights:

|                        User page                        |                      Account page                       |
| :-----------------------------------------------------: | :-----------------------------------------------------: |
| ![Design Draft1](../.github/assets/frontend/draft1.png) | ![Design Draft2](../.github/assets/frontend/draft2.png) |

These insights are only here to show the information required and provide
a baseline to your design choices and implementations.

The 2 screenshots do **not** represent our current dashboard nor the layout
we necessarily expect: we provide no constraints regarding the UI and design
in general, feel free to implement your own.

### Scope

The view should only be for **one** user.

You will need to leverage an open API for business data to fill in the details
and functionality as described below.

For simplicity reasons and in order for the test not to be too long to complete,
you are only required to develop the page to fit the viewport of the device of
your choice: either **mobile** or **desktop**.

## Delivery

At Mansa, we're big fans of React. Our stack consists of TypeScript, React,
[Next.js](https://nextjs.org/), CSS-in-JS with [styled-component](https://styled-components.com/),
Flex & Grid, and we test with Jest and Cypress.

The bare minimum is to complete the task with React. If you're comfortable with
it, we encourage you to complete the test in the stack described above.

You're also free to use a component library to get you started and any other
package that you might think is necessary.

Static type checking is a great way to introduce additional level of safety
into your code and we welcome solutions written in TypeScript, but JavaScript
is good too.

The use of component libraries, like Material UI, might make this easier and
quicker for you but keep in mind that using them means we'll have less code
to assess your knowledge and Frontend skills.

We expect you to test your code: the minimum requirement is unit tests,
end-to-end tests are a big plus. From our experience Cypress.js works very well
for React application testing, but you're free to pick your favourite.

Some remarks:

-   Use es6 or later, do not use es5
-   Do **not** use jQuery
-   Feel free to use vanilla css, CSS-in-JS, or utility-first libraries

### What We Care About

We're interested in your method and how you approach the problem just as much
as we're interested in the end result.

Here's what you should strive for:

-   Good use of current HTML, CSS, and JavaScript / TypeScript
-   A keen eye for UX and user-friendly UI, without forgetting accessibility
-   A consistent architecture, focused on the simplicity of the project
    (**keep it simple!**), pragmatism, no over-engineering
-   Extensible code
-   Clean code using proper programming patterns and JavaScript best practices

## The Weapons we provide you

### French government API

For business information, you'll have use the French SIRENE public API,
you can find the documentation about it [here](https://entreprise.data.gouv.fr/api_doc/sirene).

You can retrieve the information about a business by using the following URL:
`https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales/:siren`

> The `unites_legales` object contains all the necessary information.

For example, [here is the API link](https://entreprise.data.gouv.fr/api/sirene/v3/unites_legales/852379890)
that gives you the SIRENE profile of MansaGroup:

You can choose any SIREN (legal id) you want for your test.

### Kanedama API

For financial information, you'll use a custom API:

| Method  | Endpoint                                                            | Description                                                                                                                                                                                                                                                                        |
| ------- | ------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **GET** | /accounts                                                           | Fetch all bank accounts from a _test user_                                                                                                                                                                                                                                         |
| **GET** | /accounts/:account*id/transactions?from=\_start_date*&to=_end_date_ | Fetch the specified _account_id_ transactions from the _start_date_ to the _end_date_. Date are ISO 8601 UTC, so for example `2018-08-13T03:24:00` It can't return more than **365 days** of transactions. If there are no date specified, the oldest transaction will be returned |

**Root endpoint is: https://kata.getmansa.com/**

You can see our [Backend test README](../backend/README.md) if you want
more information about this endpoint.

### The final words

Here is a list of _nice-to-have_ bonuses is you may:

-   Write **clear documentation** on how the app was designed and how to
    run the code
-   Provide e2e tests
-   Typescript
-   Beautiful charts
-   Write concise and clear commit messages
-   Provide an online demo of the application, in a deployed environment
-   User-friendly and clear UI
-   Complete user information (Profil picture, phone number, etc ...) with
    another API like [randomuser](https://randomuser.me)
-   Describe optimization opportunities and next steps as you conclude
