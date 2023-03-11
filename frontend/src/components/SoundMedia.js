import React, { useRef, useEffect, useState } from "react";
import ReactAudioPlayer from "react-audio-player";

const SoundMedia = (props) => {
  let { sound1, sound2, fadein1, fadeout1, fadein2, fadeout2, loop } = props;
  const defaultSecond = 1;

  const [currentSound1, setCurrentSound1] = useState(null);
  const [currentSound2, setCurrentSound2] = useState(null);
  const [curFadein1, setCurFadein1] = useState(defaultSecond);
  const [curFadein2, setCurFadein2] = useState(defaultSecond);
  const [curFadeout1, setCurFadeout1] = useState(defaultSecond);
  const [curFadeout2, setCurFadeout2] = useState(defaultSecond);
  const [oldSoundGot, setOldSoundGot] = useState(false);
  const [new1, setNew1] = useState(false);
  const [new2, setNew2] = useState(false);

  useEffect(() => {
    if (sound1 !== sound2) {
      if (sound1 !== currentSound1 || (sound1 !== sound2 && !sound2)) { 
        setNew1(true);
      }
      else { 
        setNew1(false); 
      }
      
      if (currentSound1 && currentSound2 && (currentSound2 === sound1 || currentSound1 === sound2)) {
        setNew2(false);
      }
      else { 
        setNew2(true); 
      }
    
      if (currentSound1 && currentSound1 == sound2) {
        setCurFadein1(fadein2 || defaultSecond);
        setCurFadein2(fadein1 || defaultSecond);
        setCurFadeout1(fadeout2 || defaultSecond);
        setCurFadeout2(fadeout1 || defaultSecond);
      }
      else if (currentSound1 && currentSound2 && (currentSound2 == sound1 || currentSound1 == sound2)) {
        setOldSoundGot(true);
        setCurrentSound1(sound2);
        setCurrentSound2(sound1);
        setCurFadein1(fadein2 || defaultSecond);
        setCurFadein2(fadein1 || defaultSecond);
        setCurFadeout1(fadeout2 || defaultSecond);
        setCurFadeout2(fadeout1 || defaultSecond);
      } else {
        setOldSoundGot(false);
        setCurrentSound1(sound1);
        setCurrentSound2(sound2);
        setCurFadein1(fadein1 || defaultSecond);
        setCurFadein2(fadein2 || defaultSecond);
        setCurFadeout1(fadeout1 || defaultSecond);
        setCurFadeout2(fadeout2 || defaultSecond);
      }
    }
  }, [sound1, sound2]);


  const [vol1, setVol1] = useState(1);
  const [vol2, setVol2] = useState(1);

  const s1 = useRef();
  const s2 = useRef();

  const minStep = 1;
  const maxStep = 100;
  const [step1, setStep1] = useState(100);
  const [step2, setStep2] = useState(100);
  const [fade1, setFade1] = useState(false);
  const [fade2, setFade2] = useState(false);
  const getDelay = (time) => (time * 1000) / maxStep;

  useEffect(() => {
    if (sound1 !== sound2) {
      changedSound(sound1, setFade1, setVol1);
      changedSound(sound2, setFade2, setVol2);
    }
  }, [sound1, sound2]);

  const changedSound = (sound, setFade, setVol) => {
    if (sound) {
      setFade(true);
    } else {
      setFade(false);
      setVol(0);
    }
  };

  useEffect(() => {
    if (fade1) {
      setTimeout(
        () => FadeAudios(step1, setStep1, setVol1, new1), new1 ? getDelay(curFadein1) : getDelay(curFadeout2)
      );
    }
    if (fade2) {
      setTimeout(
        () => FadeAudios(step2, setStep2, setVol2, new2), new2 ? getDelay(curFadein2) : getDelay(curFadeout1)
      );
    }
  }, [fade1, fade2, step1, step2]);

  useEffect(() => {
      if (step1 >= maxStep) {
        setFade1(false);
        setStep1(minStep);
      }
      if (step2 >= maxStep) {
        setFade2(false);
        setStep2(minStep);
      }
  }, [step1, step2]);

  const FadeAudios = (step, setStep, setVol, isnew) => {
    let reverse = maxStep - step;
    if (reverse < 0) reverse = 0;

    if (isnew) {
      setVol(step / 100);
    } else {
      setVol(reverse / 100);
    }
    setStep(step + 1);
  };

  const pauseIt = () => {
    if (!new1 && vol1 == 0) {
      s1.current.audioEl.current.load();
      s1.current.audioEl.current.pause();
    } else {s1.current.audioEl.current.play();};
    if (!new2 && vol2 == 0) {
      s2.current.audioEl.current.load();
      s2.current.audioEl.current.pause();
    } else {s2.current.audioEl.current.play()};
  }
  

  return (
    <div>
      <div>
        {sound1 && (
          <ReactAudioPlayer
            src={currentSound1}
            id={1}
            autoPlay={true}
            controls
            volume={vol1}
            ref={s1}
            loop={loop}
            onVolumeChanged={() => {
              if (!new1 && vol1 == 0) {pauseIt();} 
            }}
          />
        )}

        {sound2 && (
          <ReactAudioPlayer
            src={currentSound2}
            id={2}
            autoPlay={true}
            controls
            volume={vol2}
            ref={s2}
            loop={loop}
            onVolumeChanged={() => {
              if (!new2 && vol2 == 0) {pauseIt();}
            }}
          />
        )}
      </div>
      <div className="d-flex">
        <p>vol1: {vol1} |</p>
        <p> vol2: {vol2} </p>
      </div>
      <div className="d-flex">
        <p>step1: {step1} |</p>
        <p> step2: {step2} </p>
      </div>
      <div className="d-flex">
        <p>fade1: {fade1.toString()} | </p>
        <p> fade2: {fade2.toString()} </p>
      </div>
      <div className="d-flex">
        <p>sound1: {sound1} |</p>
        <p> sound2: {sound2}</p>
      </div>
    </div>
  );
};

export default SoundMedia;