// I heard you like constants so here are some constants for defining your constants
const basePayment = "$2.00";
const bonusPerCorrectAnswerCents = 1;
const maxBonus = "$1.00";
const speededTimeSeconds = 5;

const consentText = `<p class="consent-text" style="text-align: center"><strong>CONSENT</strong></p>

<p class="consent-text"><strong>DESCRIPTION:</strong> You are invited to participate in a research study on human reasoning. We will ask you to answer a series of questions in order to learn how people reason. You will be asked to think about problems and answer by pressing buttons or writing text, and possibly explaining your reasoning into a microphone. Participation in this research is voluntary, and you are free to withdraw your consent at any time.</p>

<p class="consent-text"><strong>TIME INVOLVEMENT:</strong> Your participation will take approximately 10 minutes.</p>

<p class="consent-text"><strong>PAYMENTS:</strong> You will receive ${basePayment} as payment for your participation, as well as a bonus of up to ${maxBonus} depending on your performance.</p>

<p class="consent-text"><strong>PRIVACY AND CONFIDENTIALITY:</strong> The risks associated with this study are minimal. Study data will be stored securely, in compliance with Stanford University standards, minimizing the risk of confidentiality breach. Your individual privacy will be maintained during the research and in all published and written data resulting from the study.</p>

<p class="consent-text"><strong>CONTACT INFORMATION:</strong></p>
<p class="consent-text"><emph>Questions:</emph> If you have any questions, concerns or complaints about this research, its procedures, risks and benefits, contact <strong>Ben Prystawski</strong> (<a href="mailto://benpry@stanford.edu">benpry@stanford.edu</a>) or the Protocol Director, Noah Goodman (ngoodman@stanford.edu).</p>

<p class="consent-text"><strong>Independent Contact:</strong> If you are not satisfied with how this study is being conducted, or if you have any concerns, complaints, or general questions about the research or your rights as a participant, please contact the Stanford Institutional Review Board (IRB) to speak to someone independent of the research team at 650-723-2480 or toll free at 1-866-680-2906, or email at irbnonmed@stanford.edu. You can also write to the Stanford IRB, Stanford University, 1705 El Camino Real, Palo Alto, CA 94306.</p>

<p class="consent-text">Please save or print a copy of this page for your records.</p>

<p class="consent-text">If you agree to participate in this research, please click "I agree" below.</p>`;

const getInstructionPages = (condition) => {
  const instructionPages = [
    `
<div class="instructions">
<p>This is an experiment on human learning and reasoning. You will learn about a machine and make predictions about how it behaves.</p>
    <p>The machine has five lights of different colors. The lights are connected to each other with the following structure:</p>
    <img src="assets/connection-structure.svg">
    <p>Red and Green are connected, Green and Yellow are connected, Yellow and Blue are connected, and Blue and Purple are connected. You will be able to see this diagram throughout the experiment to help you remember the connection structure.</p>
    <p>When two lights are connected, they might <strong>support</strong> each other or they might <strong>inhibit</strong> each other.</p>
    <p>When lights support each other, they tend to be either on or off at the same time. Here is an example of two lights that support each other: they are both on at the same time.</p>
    <img style="width:40ch;margin:0 100px;" src="assets/supporting-example.png">
    <p>When lights inhibit each other, one light tends to be off when the other is on. Here is an example of two lights that inhibit each other:</p>
    <img style="width:40ch;margin:0 100px;" src="assets/inhibiting-example.png">
    <p>These are just examples of what you might see. They don't tell you anything about the behavior of the machine in the main experiment.</p>
</div>
`,
    `
<div class="instructions">
  <p>The experiment has two phases: a <strong>learning</strong> phase and a <strong>prediction phase</strong>.</p>
  <p>In the learning phase, you will see pairs of lights that are next to each other and be asked to predict whether one light is on or off given the value of another. After making each prediction, you will get feedback on whether your prediction was right or not. This phase will repeat until you are at least 90% accurate for 32 predictions in a row.</p>
  <p>In the prediction phase you will have to make predictions about <strong>all pairs of lights</strong>, including ones that you didn't see together in the learning phase. You will not get feedback on your predictions in this phase. For example, you might need to predict whether Blue is on or off given that Red is on:</p>
  <img style="width:40ch;margin:0 100px;" src="assets/example-query.png">
  <p>Please do not take notes or use them during this experiment.</p>
  <p>A random trial in prediction phase will be the <strong>bonus trial</strong>. If you get the correct answer on the bonus trial, you will earn a bonus of ${maxBonus}.</p>
</div>`,
  ];

  if (condition == "verbal-protocol") {
    instructionPages.push(`<div class="instructions">
<p>When you are making predictions, please <strong>describe your thinking aloud</strong> into your microphone. Your voice will only be recorded in the prediction phase, not the learning phase.<p/>
<p>In the next page, we will ask for permission to use your microphone and you will be able to select which recording device you want to use.</p>
</div>`);
  }

  instructionPages[instructionPages.length - 1] = instructionPages[
    instructionPages.length - 1
  ].concat(`<p>Press 'Next' to continue with the experiment.</p>`);

  return instructionPages;
};

const getDoneLearningPages = (condition) => {
  let doneLearningMessage = `<div class='instructions'>
    <p>You have completed the learning phase. Now, you will start making predictions about new pairs of lights.</p>
`;
  if (condition == "verbal-protocol") {
    doneLearningMessage = doneLearningMessage.concat(
      "<p class='instructions-text'>Remember to explain your reasoning aloud as you make predictions.</p>",
    );
  }

  if (condition == "speeded") {
    doneLearningMessage = doneLearningMessage.concat(
      `<p>You will only have <strong>${speededTimeSeconds} seconds</strong> to answer to each question. If you do not answer in ${speededTimeSeconds} seconds, the experiment will move on to the next question.</p>`,
    );
  }
  doneLearningMessage = doneLearningMessage.concat(
    `<p>Press 'Next' to begin making predictions about new pairs of lights.</p>
  </div>`,
  );

  return [doneLearningMessage];
};

const names = {
  A: "Red",
  B: "Green",
  C: "Yellow",
  D: "Blue",
  E: "Purple",
};

const stimulusSentences = {
  1: "%NAME% is on.",
  0: "%NAME% is off.",
  "?": "Is %NAME% on or off?",
};

const stimulusTemplate = `
<div class="stimulus">
  <img style="width:450px;" src="assets/connection-structure.svg">
  <p>You observe two lights.</p>
  <div class="stimulus-wrapper">
    <div class="top-left">%TEXT1%</div>
    <div class="top-right">%TEXT2%</div>
    <div class="bottom-left">
      <img src="assets/%NAME1%-%TRUTH1%.svg">
    </div>
    <div class="bottom-right">
      <img src="assets/%NAME2%-%TRUTH2%.svg">
    </div>
  </div>
  <div class="feedback">
  %FEEDBACK%
  </div>
</div>
`;
