// The Fisher-Yates shuffle implementation that everyone has to copy-paste from
// StackOverflow because JavaScript doesn't have a built-in shuffle function.
// Code from here: https://stackoverflow.com/a/2450976
function shuffle(array) {
  let currentIndex = array.length,
    randomIndex;

  // While there remain elements to shuffle.
  while (currentIndex > 0) {
    // Pick a remaining element.
    randomIndex = Math.floor(Math.random() * currentIndex);
    currentIndex--;

    // And swap it with the current element.
    [array[currentIndex], array[randomIndex]] = [
      array[randomIndex],
      array[currentIndex],
    ];
  }

  return array;
}

// range function, from here: https://stackoverflow.com/a/10050831
function range(size, startAt = 0) {
  return [...Array(size).keys()].map((i) => i + startAt);
}

function formatStimulus(
  observedVar,
  observedVal,
  targetVar,
  targetVal,
  lastTrialCorrect,
) {
  let stimulusString = stimulusTemplate;
  stimulusString = stimulusString.replace(
    `%TEXT1%`,
    stimulusSentences[observedVal].replace("%NAME%", names[observedVar]),
  );
  stimulusString = stimulusString.replace(
    `%NAME1%`,
    names[observedVar].toLowerCase(),
  );
  stimulusString = stimulusString.replace(
    `%TRUTH1%`,
    observedVal == 1 ? "on" : "off",
  );
  stimulusString = stimulusString.replace(
    `%NAME2%`,
    names[targetVar].toLowerCase(),
  );
  stimulusString = stimulusString.replace(
    "%TEXT2%",
    stimulusSentences["?"].replace("%NAME%", names[targetVar]),
  );
  stimulusString = stimulusString.replace(
    `%TRUTH2%`,
    targetVal == 1 ? "on" : targetVal == "?" ? "question-mark" : "off",
  );
  if (lastTrialCorrect === undefined) {
    stimulusString = stimulusString.replace(`%FEEDBACK%`, "");
  } else if (lastTrialCorrect) {
    stimulusString = stimulusString.replace(
      `%FEEDBACK%`,
      `<p class='feedback-correct'>Correct! ${stimulusSentences[
        targetVal
      ].replace("%NAME%", names[targetVar])}</p>`,
    );
  } else {
    stimulusString = stimulusString.replace(
      `%FEEDBACK%`,
      `<p class='feedback-incorrect'>Incorrect. ${stimulusSentences[
        targetVal
      ].replace("%NAME%", names[targetVar])}</p>`,
    );
  }
  return stimulusString;
}
