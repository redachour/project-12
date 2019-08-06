# project-12
social team builder

Hello i'm redha achour, and i'll talk about some more plugings and a custom workflow that we created to automatically create payment 
records each time a mortgage is approved, because we can't excecute that business logic on our dynamics UI,
so we opted for custom worflow over a plugin because we need some dynamics input from mortgage entity like mortgage 
term and monthly payment to make a loop that create records based on mortgage term, so each month represent one record and
the due date increment each time by one month but the monthly payment of course stay the same for all payment records, and on 
our Dynamics UI we created an on demand workflow with our custom workflow as a step and append it to our mortgage business process
flow on the approval stage.
