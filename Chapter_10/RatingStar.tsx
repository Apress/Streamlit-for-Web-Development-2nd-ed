import {
   Streamlit,
   StreamlitComponentBase,
   withStreamlitConnection,
}  from 'streamlit-component-lib'
import React, { ReactNode } from 'react'
import { Rating } from '@mui/material'
interface State {}
class RatingStar extends StreamlitComponentBase<State> {
  public state = {}
  public render = (): ReactNode => {
    const { selected, stars_count } = this.props.args
    return (
     <Rating
       size='large'
       defaultValue={1}
       max={stars_count}
       onChange={(_, stars_count) => Streamlit.setComponentValue(stars_count)}
     />
    )
  }
}
export default withStreamlitConnection(RatingStar)
